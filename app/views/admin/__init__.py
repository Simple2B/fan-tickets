from .admin import admin_blueprint
from .location import location_blueprint
from .category import category_blueprint
from .event import event_blueprint
from .users import blueprint_user

admin_blueprint.register_blueprint(location_blueprint)
admin_blueprint.register_blueprint(category_blueprint)
admin_blueprint.register_blueprint(event_blueprint)
admin_blueprint.register_blueprint(blueprint_user)
