# Frontend example

In waiting for an integrated solution, here is an example to display a map
rendered by `wagtail_maps.blocks.MapBlock`.

It uses the following:
- [Leaflet] to display the map and its points
- [Bootstrap] for the UI (optional), custom styles for Leaflet can be found
  in [`scss/_leaflet.scss`](scss/_leaflet.scss) to integrate the popups and
  other elements with your theme
- [Webpack] to compile and split the JavaScript code (optional)

[Leaflet]: https://leafletjs.com
[Bootstrap]: https://getbootstrap.com
[Webpack]: https://webpack.js.org
