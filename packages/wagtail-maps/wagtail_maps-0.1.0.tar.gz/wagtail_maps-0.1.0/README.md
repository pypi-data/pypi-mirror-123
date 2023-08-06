# wagtail-maps

Create and display maps with points in Wagtail.

**Warning!** This project is still early on in its development lifecycle. It is
possible for breaking changes to occur between versions until reaching a stable
1.0. Feedback and pull requests are welcome.

This package extend Wagtail to add a new Map model, which is composed by one or
more points. Each point may have a title, some content and link to an internal
or external URL. Once you have configured your map from the Wagtail admin, you
will be able to display it in a page - e.g. as a StreamField block.

## Requirements

This package requires the following:
- **Wagtail >= 2.14**: upstream patches have been submitted to provide a proper
  integration of this extension into the admin - see [#7562], [#7565] and
  [#7590]
- **Django** (3.1, 3.2)
- **Python 3** (3.7, 3.8, 3.9)

[#7562]: https://github.com/wagtail/wagtail/pull/7562
[#7565]: https://github.com/wagtail/wagtail/pull/7565
[#7590]: https://github.com/wagtail/wagtail/pull/7590

## Installation

1. Install using ``pip``:
   ```shell
   pip install wagtail-maps
   ```
2. Add ``wagtail_maps`` to your ``INSTALLED_APPS`` setting:
   ```python
   INSTALLED_APPS = [
       # ...
       'wagtail_maps',
       # ...
   ]
   ```
3. Include the URL of *wagtail-maps* to your ``urls.py`` file:
   ```python
   from wagtail_maps import urls as wagtailmaps_urls

   urlpatterns = [
       # ...
       path('maps/', include(wagtailmaps_urls)),
       # ...
   ]
   ```
4. Run ``python manage.py migrate`` to create the models

## Usage

A StreamField block `wagtail_maps.blocks.MapBlock` can be used to display a
map - choosen from the current ones - in your page. The JavaScript code and the
Leaflet package is currently not shipped, but you can find an example in
[examples/frontend/](examples/frontend/).

## Development
### Quick start

To set up a development environment, ensure that Python 3 is installed on your
system. Then:

1. Clone this repository
2. Create a virtual environment and activate it:
   ```shell
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install this package in develop mode with extra requirements:
   ```shell
   pip install -e .[test]
   ```

### Contributing

The Python code is formatted and linted thanks to [flake8], [isort] and [black].
To ease the use of this tools, the following commands are available:
- `make lint`: check the Python code syntax and imports order
- `make format`: fix the Python code syntax and imports order

The tests are written with [pytest] and code coverage is measured with [coverage].
You can use the following commands for that:
- ``make test``: run the tests and output a quick report of code coverage
- ``make coverage``: run the tests and produce an HTML report of code coverage

When submitting a pull-request, please ensure that the code is well formatted
and covered, and that all the other tests pass.

[flake8]: https://flake8.pycqa.org/
[isort]: https://pycqa.github.io/isort/
[black]: https://black.readthedocs.io/
[pytest]: https://docs.pytest.org/
[coverage]: https://coverage.readthedocs.io/

## License

This extension is mainly developed by [Cliss XXI](https://www.cliss21.com) and
licensed under the [AGPLv3+](LICENSE). Any contribution is welcome!
