function startTime() {
  var today = new Date();

  document.getElementById('time').innerHTML = "Die Uhrzeit ist: " +
  today.toLocaleTimeString('de-De', hour12=false);

  document.getElementById('date').innerHTML = "Das Datum ist: " +
  today.toLocaleDateString('de-De');

  var t = setTimeout(startTime, 500);
}

function set_zero(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
}
