import nuke
import os

import re

TOKENS = (r"#+", r"%0\d+d")  # image.%04d.exr - percent

TOKEN_RX = re.compile("|".join(TOKENS), re.IGNORECASE)


def divider(submitter, name):
    """
    UI horizontal rule.
    """
    k = nuke.Text_Knob(name, "", "")
    submitter.addKnob(k)


def eval_star_path(knob):
    value = knob.value().replace("'", "\\'")
    if not value:
        return None
    try:
        value = nuke.runIn(knob.node().fullName(), "nuke.tcl('return {}')".format(value))
    except:
        pass
    if not value:
        return None
    if not os.path.isabs(value):
        value = os.path.join(nuke.script_directory(), value)
    value = TOKEN_RX.sub("*", value)
    return value


def truncate_path_to_star(in_path):
    """
    Make sure the path contains no wildcards (stars).

    If it does, truncate the path up to the component containing the star.

    Args:
        in_path (str): The path to examine.

    Returns:
        [str]: Possibly truncated path
    """

    result = in_path
    while True:
        if not "*" in result:
            return result
        result = os.path.dirname(result)
