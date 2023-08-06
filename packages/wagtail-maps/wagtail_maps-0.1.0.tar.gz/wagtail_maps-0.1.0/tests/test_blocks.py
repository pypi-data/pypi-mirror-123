import pytest
from pytest_django.asserts import assertHTMLEqual

from wagtail_maps.blocks import MapBlock

from .factories import MapFactory


@pytest.mark.django_db
class TestMapBlock:
    @pytest.fixture(autouse=True)
    def setup_block(self):
        self.block = MapBlock()
        self.block.set_name('test_mapblock')

    def render(self, data):
        return self.block.render(self.block.to_python(data))

    def test_form_response_map(self):
        maps = MapFactory.create_batch(2)

        value = self.block.value_from_datadict({'p-map': maps[1].pk}, {}, 'p')
        assert value['map'] == maps[1]

    @pytest.mark.parametrize('value', ('', None, '10'))
    def test_form_response_map_none(self, value):
        MapFactory.create_batch(2)

        value = self.block.value_from_datadict({'p-map': value}, {}, 'p')
        assert value['map'] is None

    def test_render(self):
        assertHTMLEqual(
            self.render(
                {
                    'map': MapFactory(
                        center_latitude=0.0, center_longitude=1.0
                    ).id
                }
            ),
            """
            <div class="map" data-map
              data-map-api-url="/maps/api/v1/1/"
              data-map-center-lat="0.0000"
              data-map-center-lng="1.0000">
            </div>
            """,
        )

    def test_render_with_attrs(self):
        assertHTMLEqual(
            self.render(
                {
                    'map': MapFactory(
                        center_latitude=0.0, center_longitude=1.0, min_zoom=2
                    ).id,
                    'zoom': '1',
                    'height': '10',
                }
            ),
            """
            <div class="map" data-map
              data-map-api-url="/maps/api/v1/1/"
              data-map-center-lat="0.0000"
              data-map-center-lng="1.0000"
              data-map-height="10"
              data-map-min-zoom="2"
              data-map-zoom="1">
            </div>
            """,
        )

    def test_render_unknown(self):
        assert self.render({'map': '100'}) == ''
