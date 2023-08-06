from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    HelpPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.contrib.modeladmin.options import ModelAdmin

from .models import Map


class MapAdmin(ModelAdmin):
    model = Map
    menu_icon = 'map'
    list_display = ('name', 'points_count')
    form_view_extra_css = ['wagtail_maps/css/admin-form.css']
    form_view_extra_js = ['wagtail_maps/js/admin-form.js']

    panels = [
        FieldPanel('name', classname='title'),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel('center_latitude', heading=_("Latitude")),
                        FieldPanel('center_longitude', heading=_("Longitude")),
                    ]
                ),
                HelpPanel(
                    template='wagtail_maps/edit_handlers/center_calculate.html'
                ),
            ],
            heading=_("Center of the map"),
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel('min_zoom', heading=_("Minimum")),
                        FieldPanel('max_zoom', heading=_("Maximum")),
                    ]
                )
            ],
            heading=_("Zoom levels"),
        ),
        InlinePanel(
            'points',
            panels=[
                FieldPanel('title'),
                FieldPanel('content'),
                PageChooserPanel('page_link'),
                FieldPanel('external_link'),
                FieldRowPanel(
                    [FieldPanel('latitude'), FieldPanel('longitude')]
                ),
                HelpPanel(
                    template='wagtail_maps/edit_handlers/point_from_geo.html'
                ),
            ],
            heading=_("Points"),
            label=_("Point"),
            min_num=1,
        ),
    ]

    def points_count(self, obj):
        return obj.points.count()

    points_count.short_description = _("Points")
