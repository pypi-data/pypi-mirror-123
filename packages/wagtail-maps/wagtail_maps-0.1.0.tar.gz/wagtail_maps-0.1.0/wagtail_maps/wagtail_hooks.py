from wagtail.contrib.modeladmin.options import modeladmin_register
from wagtail.core import hooks

from .admin import MapAdmin

modeladmin_register(MapAdmin)


@hooks.register('register_icons')
def register_icons(icons):
    icons.append('wagtail_maps/icons/map.svg')
    return icons
