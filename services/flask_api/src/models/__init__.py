from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .user_models import *
from .location_models import *
from .account_models import *
from .menu_models import *
from .product_models import *
