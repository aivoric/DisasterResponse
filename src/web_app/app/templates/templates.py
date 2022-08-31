from fastapi.templating import Jinja2Templates
import os

def get_templates():
    template_location = os.path.dirname(os.path.realpath(__file__))
    templates = Jinja2Templates(directory=template_location)
    return templates