from flask import Blueprint

acceso=Blueprint(
    'acceso',
    __name__,
    template_folder='templates',
    static_folder='static')
from . import routes
