function startTime() {
  var today = new Date();
  document.getElementById('time').innerHTML = today.toLocaleTimeString('de-De',
                                                                       hour12=false);
  document.getElementById('date').innerHTML = today.toLocaleDateString('de-De');

  var t = setTimeout(startTime, 500);
}
