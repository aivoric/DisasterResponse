from fastapi.templating import Jinja2Templates
import os

def get_templates():
    template_files = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../templates")
    templates = Jinja2Templates(directory=template_files)
    return templates