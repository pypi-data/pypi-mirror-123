"""
Row of buttons at the top of the submitter.
"""
import os

import nuke
from ciocore import data as coredata


from cionuke import const as k
from cionuke import submit
from cionuke.components import instance_type, project, software

FIXTURES_DIR = os.path.expanduser(os.path.join("~", "conductor_fixtures"))


def build(submitter):
    """Build action knobs."""

    knob = nuke.PyScript_Knob("cio_connect", "Connect")
    submitter.addKnob(knob)

    knob = nuke.PyScript_Knob("cio_validate", "Validate")
    submitter.addKnob(knob)


    knob = nuke.PyScript_Knob("cio_submit", "Submit")
    submitter.addKnob(knob)


def knobChanged(node, knob):
    """
    Respond to button pushes.
    """
    knob_name = knob.name()
    if knob_name == "cio_connect":
        connect(node)
    elif knob_name == "cio_validate":
        submit.submit(node, submitting=False)
    elif knob_name == "cio_submit":
        submit.submit(node, submitting=True)


def affector_knobs():
    """Knobs will affect the payload when changed."""
    return ["inputChange", "cio_connect"]

def connect(submitter):
    """
    Connect to Conductor in order to access users account data.

    Menus must be repopulated.
    """

    coredata.init(product="nuke")
    if k.FEATURE_DEV:
        use_fixtures = submitter.knob("cio_use_fixtures").getValue()
        fixtures_dir = FIXTURES_DIR if use_fixtures else None
        coredata.set_fixtures_dir(fixtures_dir)

    try:
        coredata.data(force=True)
    except BaseException as ex:
        print(str(ex))
        print("Try again after deleting your credentials file (~/.config/conductor/credentials)")
    if coredata.valid():
        project.rebuild_menu(submitter, coredata.data()["projects"])
        instance_type.rebuild_menu(submitter, coredata.data()["instance_types"])
        software.rebuild_menu(submitter, coredata.data().get("software"))
