function isNumber(value) {
  return value === Number(value).toString();
}

function add(accumulator, a) {
  return accumulator + a;
}

document.addEventListener('DOMContentLoaded', () => {
  const latInput = document.getElementById('id_center_latitude');
  const lngInput = document.getElementById('id_center_longitude');
  const calcButton = document.getElementById('map-center-calculate');
  const errorMessage = calcButton.nextElementSibling;

  calcButton.addEventListener('click', () => {
    const lat = [];
    const lng = [];

    errorMessage.setAttribute('hidden', '');

    [].slice.call(document.querySelectorAll('#id_points-FORMS > li:not(.deleted)'))
      .forEach(function (child) {
        const latitude = child.querySelector('[name$=-latitude]').value;
        const longitude = child.querySelector('[name$=-longitude]').value;

        if (isNumber(latitude) && isNumber(longitude)) {
          lat.push(Number(latitude));
          lng.push(Number(longitude));
        }
      });

    if (!lat.length) {
      errorMessage.removeAttribute('hidden');
      return;
    }

    latInput.value = lat.reduce(add) / lat.length;
    lngInput.value = lng.reduce(add) / lng.length;
  });
});
