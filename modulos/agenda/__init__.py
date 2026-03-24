from flask import Blueprint

agenda=Blueprint(
    'agenda',
    __name__,
    template_folder='templates',
    static_folder='static')
from . import routes
