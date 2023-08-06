document.addEventListener('DOMContentLoaded', () => {
  const mapContainers = [].slice.call(document.querySelectorAll('[data-map]'));

  if (mapContainers.length) {
    import(/* webpackChunkName: "map" */ './map').then((module) => {
      const Map = module.default;

      mapContainers.forEach((element) => new Map(element));
    });
  }
});
