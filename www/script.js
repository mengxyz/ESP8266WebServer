document.addEventListener('DOMContentLoaded', function () {
    var relay1 = document.querySelector('input[id="relay1"]');
    var relay2 = document.querySelector('input[id="relay2"]');
    relay1.addEventListener('change', function () {
        swit_relay1();
    });
    relay2.addEventListener('change', function () {
        swit_relay2();
    });
});

function swit_relay1() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var relay1 = document.querySelector('input[id="relay1"]');
            if (this.responseText == "r1_On") {
                relay1.checked = true;
            }
            else if (this.responseText == "r1_Off") {
                relay1.checked = false;
            }
            console.log(this.responseText);
        }
    };
    xhttp.open("GET", "/switch?val=1", true);
    xhttp.send();
}

function swit_relay2() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var relay1 = document.querySelector('input[id="relay2"]');
            if (this.responseText == "r2_On") {
                relay1.checked = true;
            }
            else if (this.responseText == "r2_Off") {
                relay1.checked = false;
            }
            console.log(this.responseText);
        }
    };
    xhttp.open("GET", "/switch?val=2", true);
    xhttp.send();
}

function moter(val) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/moter?val=" + val, true);
    xhttp.send();
}

function get_current_state() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            state = JSON.parse(this.responseText);
            if (state.relay1 == 1) {
                document.getElementById("relay1").checked = false;
            } else {
                document.getElementById("relay1").checked = true;
            }
            if (state.relay2 == 1) {
                document.getElementById("relay2").checked = false;
            } else {
                document.getElementById("relay2").checked = true;
            }
            if(state.moter > -1){
                document.getElementById("range_in").value = state.moter;
                document.getElementById("range_out").innerHTML = state.moter;
            }

        }
    };
    xhttp.open("GET", "/get_state", true);
    xhttp.send();
}

var slider = document.querySelector('input[id="range_in"]');
slider.value = 0;
var output = document.querySelector('span[id="range_out"]');
slider.addEventListener('input', function () {
    output.innerHTML = this.value;
});
slider.addEventListener('change', function () {
    moter(this.value);
});

var page = 0;
setInterval(function () {
    if (page == 1) {
        get_current_state();
        page = 0;
    }
    page++;
}, 1000);

new TypeIt('#header', {
    speed: 200,
    waitUnitVisible: true
})
    .type('Esp ')
    .pause(500)
    .type('8255')
    .pause(500)
    .delete(2)
    .type('66')
    .break()
    .type('Java Ajax Jquery')
    .break()
    .type('<strong>Test</strong>')
    .go()
    ;