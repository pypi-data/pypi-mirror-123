import L from 'leaflet';

/**
 * ------------------------------------------------------------------------
 * Constants
 * ------------------------------------------------------------------------
 */

const NAME = 'map';

const Default = {
  apiUrl: null,
  centerLat: null,
  centerLng: null,
  height: 400,
  mapPadding: 10,
  maxZoom: null,
  minZoom: null,
  popupOptions: {
    minWidth: 80,
    closeButton: false,
  },
  tooltipOptions: { opacity: 1 },
  zoom: 8,
};

const DefaultType = {
  apiUrl: 'string',
  centerLat: 'number',
  centerLng: 'number',
  height: 'number',
  mapPadding: 'number',
  maxZoom: 'number|null',
  minZoom: 'number|null',
  popupOptions: 'object',
  tooltipOptions: 'object',
  zoom: 'number',
};

const TileProvider = {
  url: '//{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png',
  options: {
    attribution:
      'donn&eacute;es &copy; <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
    minZoom: 1,
    maxZoom: 20,
  },
};

/**
 * ------------------------------------------------------------------------
 * Helpers
 * ------------------------------------------------------------------------
 * Most of those helpers are taken from Bootstrap, which is licensed under
 * MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE).
 */

function toType(obj) {
  if (obj === null || obj === undefined) {
    return `${obj}`;
  }

  return {}.toString
    .call(obj)
    .match(/\s([a-z]+)/i)[1]
    .toLowerCase();
}

function isElement(obj) {
  if (!obj || typeof obj !== 'object') {
    return false;
  }

  if (typeof obj.jquery !== 'undefined') {
    obj = obj[0];
  }

  return typeof obj.nodeType !== 'undefined';
}

function getElement(obj) {
  if (isElement(obj)) {
    return obj.jquery ? obj[0] : obj;
  }

  if (typeof obj === 'string' && obj.length > 0) {
    return document.querySelector(obj);
  }

  return null;
}

function typeCheckConfig(config, configTypes) {
  Object.keys(configTypes).forEach((property) => {
    const expectedTypes = configTypes[property];
    const value = config[property];
    const valueType = value && isElement(value) ? 'element' : toType(value);

    if (!new RegExp(expectedTypes).test(valueType)) {
      throw new TypeError(
        `${NAME.toUpperCase()}: Option "${property}" provided type "${valueType}" but expected type "${expectedTypes}".`
      );
    }
  });
}

function normalizeData(val) {
  if (val === 'true') {
    return true;
  }

  if (val === 'false') {
    return false;
  }

  if (val === Number(val).toString()) {
    return Number(val);
  }

  if (val === '' || val === 'null') {
    return null;
  }

  return val;
}

function getDataAttributes(element) {
  const attributes = {};

  Object.keys(element.dataset)
    .filter((key) => key.startsWith(NAME) && key !== NAME)
    .forEach((key) => {
      const name =
        key.charAt(NAME.length).toLowerCase() + key.slice(NAME.length + 1);
      attributes[name] = normalizeData(element.dataset[key]);
    });

  return attributes;
}

/**
 * ------------------------------------------------------------------------
 * Class Definition
 * ------------------------------------------------------------------------
 */

class Map {
  constructor(element, config) {
    element = getElement(element);

    if (!element) {
      return;
    }

    this._element = element;
    this._config = this._getConfig(config);

    if (!this._config.apiUrl) {
      throw new TypeError(
        `${NAME.toUpperCase()}: Option "apiUrl" must be provided.`
      );
    }

    this._map = this._initializeMap();
    this._featureGroup = L.featureGroup();
    this._featureGroup.addTo(this._map);

    this.fetch();
  }

  // Getters

  static get Default() {
    return Default;
  }

  static get TileProvider() {
    return TileProvider;
  }

  // Public

  clear() {
    this._featureGroup.clearLayers();
  }

  fetch() {
    this.clear();

    return fetch(this._config.apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error(
            `${NAME.toUpperCase()}: Unable to fetch data from the API.`
          );
        }

        return response.json();
      })
      .then(({ points }) => {
        points.forEach(this._addMarker.bind(this));
      });
  }

  // Private

  _getConfig(config) {
    config = {
      ...Default,
      ...getDataAttributes(this._element),
      ...(typeof config === 'object' ? config : {}),
    };

    typeCheckConfig(config, DefaultType);

    return config;
  }

  _initializeMap() {
    this._element.style.height = `${this._config.height}px`;

    const map = L.map(this._element, {
      center: [this._config.centerLat, this._config.centerLng],
      layers: [L.tileLayer(TileProvider.url, TileProvider.options)],
      zoom: this._config.zoom,
      zoomControl: false,
    });

    if (this._config.maxZoom) {
      map.setMaxZoom(this._config.maxZoom);
    }

    if (this._config.minZoom) {
      map.setMinZoom(this._config.minZoom);
    }

    // Add custom zoom controls
    map.zoomControl = L.control.zoom({
      zoomInText: '',
      zoomInTitle: 'Vue rapprochée',
      zoomOutText: '',
      zoomOutTitle: 'Vue éloignée',
    });
    map.addControl(map.zoomControl);

    map.on('popupopen', ({ popup }) => {
      // Listen to click on elements with `data-dismiss="popup"` within a popup
      popup.getElement().addEventListener('click', (event) => {
        if (event.target.matches('[data-dismiss="popup"]')) {
          event.preventDefault();
          map.closePopup(popup);
        }
      });
    });

    return map;
  }

  _addMarker(point) {
    const marker = L.marker([point.latitude, point.longitude]);

    if (point.content) {
      marker.bindPopup(point.content, {
        maxHeight: this._config.height - this._config.mapPadding * 2,
        ...this._config.popupOptions,
      });
    } else {
      marker.bindTooltip(point.title, this._config.tooltipOptions);

      if (point.url) {
        marker.on('click', () => {
          window.location.assign(point.url);
        });
      }
    }

    this._featureGroup.addLayer(marker);
  }
}

export default Map;
