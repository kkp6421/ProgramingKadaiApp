from flask import Blueprint

comment = Blueprint(__name__, 'comment')

from . import views