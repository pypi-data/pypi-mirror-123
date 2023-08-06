import nuke

TOOLTIPS = {
    "cio_title": "The job title shows up in the Conductor dashboard. You may use TCL expressions here.",
}
 
def build(submitter):
    """Build knobs to specify the job title."""
    knob = nuke.EvalString_Knob("cio_title", "Job title", "NUKE [file tail [value root.name]]")
    submitter.addKnob(knob)


def resolve(node, **kwargs):
    return {"job_title": node.knob("cio_title").getValue()}


def affector_knobs():
    """Knobs that affect the payload when changed."""
    return ["cio_title"]


