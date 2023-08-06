from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail.core import blocks
from wagtail.core.utils import resolve_model_string


def build_map_attrs(**config):
    attrs = {}
    for name, value in config.items():
        if value not in (None, ''):
            attrs[f'data-map-{name}'] = value
    return attrs


class MapChooserBlock(blocks.ChooserBlock):
    class Meta:
        label = _("Map")

    @cached_property
    def target_model(self):
        return resolve_model_string('wagtail_maps.Map')

    @cached_property
    def widget(self):
        return forms.Select()

    def value_from_form(self, value):
        if value == '':
            return None
        return super().value_from_form(value)


class MapBlock(blocks.StructBlock):
    map = MapChooserBlock()
    height = blocks.IntegerBlock(
        label=_("Height (px)"),
        required=False,
        min_value=10,
    )
    zoom = blocks.IntegerBlock(
        label=_("Initial zoom"),
        required=False,
        min_value=1,
        max_value=20,
    )

    class Meta:
        icon = 'map'
        label = _("Map")
        template = 'wagtail_maps/map_block.html'

    def render(self, value, context=None):
        if not value.get('map'):
            return ''
        return super().render(value, context=context)

    def get_context(self, value, **kwargs):
        context = super().get_context(value, **kwargs)
        context['attrs'] = build_map_attrs(
            **{
                'center-lat': value['map'].center_latitude,
                'center-lng': value['map'].center_longitude,
                'max-zoom': value['map'].max_zoom,
                'min-zoom': value['map'].min_zoom,
                'height': value.get('height'),
                'zoom': value.get('zoom'),
            }
        )
        return context
