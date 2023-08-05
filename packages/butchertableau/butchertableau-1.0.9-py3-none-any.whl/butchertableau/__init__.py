import os
from . import butchertableau
from .butchertableau import butcher

__all__ = ["butchertableau"] 


try:
    butcher_dir = os.path.dirname(__file__)
except:
    butcher_dir = ''