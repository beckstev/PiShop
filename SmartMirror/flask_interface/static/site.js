"use strict;"

var socket = io('http://' + document.domain + ':' + location.port);

function updateWeather(data) {
  console.log("update");
  console.log(data);
  let div = document.getElementById('weather');
  div.innerHTML = "";
  data["forecasts"].map(elem => {
    console.log(elem);
    h1 = document.createElement("h1");
    h1.innerHTML = "Weather of " + elem["day"];
    div.appendChild(h1);
  })
}


socket.on("update", updateWeather);
