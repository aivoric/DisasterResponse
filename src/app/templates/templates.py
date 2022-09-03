from fastapi.templating import Jinja2Templates
import os

def get_templates():
    """
    Gets the path to where the templates are stored.

    Returns a Jinja2Templates() templates object which can then be used to render jinja templates.
    """
    template_location = os.path.dirname(os.path.realpath(__file__))
    templates = Jinja2Templates(directory=template_location)
    return templates