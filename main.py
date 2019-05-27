import ESP8266WebServer
import network,json
from machine import Pin, PWM

STA_SSID = "your-ssid"
STA_PSK = "Meng005252"


rootPage = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <style>
        h1{
            margin: 10px auto;
            font-family: monaco,Consolas,Lucida Console,monospace; 
            color: white;
        }
        body{
            background-color: black;
        }
    </style>
</head>

<body>
    <center>
        <h1 id="count"></h1>
    </center>
    
    <script>
        function c(val,dot){
            if(val > 0){
                document.getElementById("count").innerHTML = "Redirect" + dot;
            }
            else{
                window.location = "http://192.168.4.1:8899/www/index2.html";
                //window.location = "http://www.google.com";
            }
        }
        var i = 5;
        var str = "";
        setInterval(function () {
            str += ".";
            c(i,str);
            i--;
        }, 1000);
    </script>
</body>
</html>
  """
sta_if = network.WLAN(network.STA_IF)
sta_if.active(False)

ap = network.WLAN(network.AP_IF) 
ap.active(True)        
ap.config(essid='ESP-AP')
ap.config(authmode=3, password='123456789')
print('Please connect IP http://192.168.4.1:8899')


relay1 = Pin(4, Pin.OUT)
relay2 = Pin(0, Pin.OUT)
moter = PWM(Pin(5), 50)
relay2.value(1)
relay1.value(1)


def handleRoot(socket, args):
  global rootPage
  response = rootPage
  ESP8266WebServer.ok(socket, "200", response)

def handleState(socket, args):
  print('Relay 1 :',relay1.value())
  print('Relay 2 :',relay2.value())
  print('Moter :',moter.duty())
  jason_ = {"relay1":relay1.value(),"relay2":relay2.value(),"moter":moter.duty()}
  jason_ = json.dumps(jason_)
  ESP8266WebServer.ok(socket, "200",jason_)


def handleSwitch(socket, args):
  if args['val'] == '1':
      relay1.value(not relay1.value())
      ESP8266WebServer.ok(socket, "200", "r1_On" if relay1.value() == 0 else "r1_Off")
  elif args['val'] == '2':
      relay2.value(not relay2.value())
      ESP8266WebServer.ok(socket, "200", "r2_On" if relay2.value() == 0 else "r2_Off")

def handleMoter(socket,args):
  val = int(args['val'])
  moter.duty(val)


ESP8266WebServer.begin(8899)

ESP8266WebServer.onPath("/", handleRoot)
ESP8266WebServer.onPath("/get_state", handleState)
ESP8266WebServer.onPath("/switch", handleSwitch)
ESP8266WebServer.onPath("/moter", handleMoter)


ESP8266WebServer.setDocPath("/www")

try:
  while True:
    ESP8266WebServer.handleClient()
except:
  ESP8266WebServer.close()
