"""
Controls that are beyond basic operation.
"""
import nuke
import re
import os

from cionuke import utils
from cionuke import const as k

from ciopath.gpath_list import PathList

DEFAULT_TASK_TEMPLATE = 'nuke -V 2 --remap "[value cio_pathmap]" -F [value cio_range_args] -X [python {",".join([n.name() for n in nuke.thisNode().dependencies(nuke.INPUTS | nuke.HIDDEN_INPUTS)])}] "[regsub -nocase {^[A-Z]:} [value root.name] []]"'

def build(submitter):
    """
    Build the controls.
    """
    knob = nuke.Boolean_Knob("cio_use_daemon", "Use upload daemon")
    submitter.addKnob(knob)
    knob.setValue(0)

    knob = nuke.String_Knob("cio_emails", "Email notifications", "you@vfxco.com,me@vfxco.com")
    submitter.addKnob(knob)
    knob.setEnabled(False)

    knob = nuke.Boolean_Knob("cio_use_emails", "Enable")
    knob.clearFlag(nuke.STARTLINE)
    submitter.addKnob(knob)
    knob.setValue(0)

    knob = nuke.Int_Knob("cio_retries", "Retries on preemption")
    knob.setValue(1)
    knob.setFlag(nuke.STARTLINE)
    submitter.addKnob(knob)

    nuke.knobDefault("Group.cio_task", DEFAULT_TASK_TEMPLATE)
    knob = nuke.EvalString_Knob("cio_task", "Task template")
    knob.setValue(DEFAULT_TASK_TEMPLATE)
    submitter.addKnob(knob)
    knob.setVisible(False)

    knob = nuke.Boolean_Knob("cio_use_custom_task", "Use custom task")
    knob.clearFlag(nuke.STARTLINE)
    submitter.addKnob(knob)
    knob.setValue(0)


    knob = nuke.String_Knob("cio_range_args", "Range args")
    submitter.addKnob(knob)
    knob.setVisible(False)

    knob = nuke.String_Knob("cio_location", "Location")
    submitter.addKnob(knob)

    if k.FEATURE_DEV:
        utils.divider(submitter, "advanced1")
        knob = nuke.Boolean_Knob("cio_use_fixtures", "Use fixtures")
        submitter.addKnob(knob)
        knob.setValue(0)

    utils.divider(submitter, "advanced2")

    knobChanged(submitter, submitter.knob("cio_use_custom_task"))


def knobChanged(node, knob):
    """
    Adjust the enabled/visible state of UI components in this component.
    """
    knob_name = knob.name()
    if knob_name in ["cio_use_emails", "cio_use_custom_task"]:
        use_emails = bool(node.knob("cio_use_emails").getValue())
        use_custom_task = bool(node.knob("cio_use_custom_task").getValue())
        node.knob("cio_emails").setEnabled(use_emails)
        node.knob("cio_task").setVisible(use_custom_task)
        if not use_custom_task:
            node.knob("cio_task").setValue(DEFAULT_TASK_TEMPLATE)


def resolve(submitter, **kwargs):
    """
    Resolve the part of the payload that is handled by this component.
    """
    result = {}
    result["autoretry_policy"] = {"preempted": {"max_retries": int(submitter.knob("cio_retries").getValue())}}
    result["local_upload"] = not submitter.knob("cio_use_daemon").getValue()

    location = submitter.knob("cio_location").getValue().strip()
    if location:
        result["location"] = location

    if submitter.knob("cio_use_emails").getValue():
        emails = list([_f for _f in re.split(r"[, ]+", submitter.knob("cio_emails").getValue()) if _f])
        if emails:
            result["notify"] = emails
    try:
        result["output_path"] = evaluate_output_path(submitter)
    except BaseException:
        result["output_path"] = "Invalid output paths"
    return  result


def evaluate_output_path(submitter):
    path_list = PathList()
    for node in [n for n in submitter.dependencies() if n.Class() == "Write"]:
        value = utils.eval_star_path(node.knob("file"))
        value = os.path.dirname(value)
        value = utils.truncate_path_to_star(value)
        if value:
            path_list.add(value)
    return path_list.common_path().fslash()

 


def affector_knobs():
    """knobs that affect the payload in te preview panel."""
    return [
        "cio_use_daemon",
        "cio_emails",
        "cio_use_emails",
        "cio_retries",
        "cio_use_custom_task",
        "cio_task",
        "cio_location"
    ]
