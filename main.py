import Adafruit_DHT
from gpiozero import Button, LED
import RPi.GPIO as GPIO
from subprocess import check_call
import time
import threading
from bluedot.btcomm import BluetoothServer

GPIO.setmode(GPIO.BCM)

sensor = Adafruit_DHT.DHT11
pin_sensor_hum = 18
pin_agua = 25
btn_apagar_raspi = 27
btn_leds = 22
red = LED(23)
white = LED(20)
orange = LED(21)
btn_humi = Button(17)
btn_reset = (24)
tiempo = 0
contador_activo = False
led_encendido = False

GPIO.setup(btn_leds, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def sensor_humytemp():
    hum, temp = Adafruit_DHT.read_retry(sensor, pin_sensor_hum)
    return hum, temp

def mostrar_tiempo():
    horas = tiempo // 3600
    minutos = (tiempo % 3600) // 60
    segundos = tiempo % 60
    return "{:02d}:{:02d}:{:02d}".format(horas, minutos, segundos)
     
def boton_huminificador():
    global tiempo, contador_activo
    if not contador_activo:
        tiempo = 300  # Iniciar en 5 minutos
        contador_activo = True
        print("Contador iniciado. Tiempo restante: 05:00:00")
    else:
        tiempo += 300  # Agregar 5 minutos adicionales
        print("Tiempo extendido. Tiempo restante: {:02d}:{:02d}:{:02d}".format(tiempo // 3600, (tiempo % 3600) // 60,
                                                                               tiempo % 60))

def boton_reinicio():
    global tiempo, contador_activo
    tiempo = 0  # Reiniciar el contador a cero
    contador_activo = False
    orange.off()
    
def boton_leds_apagar_y_prender(channel):
    # Lógica para apagar o encender los LEDs
    global led_encendido

    # Lógica para apagar o encender los LEDs al presionar el botón
    if led_encendido:
        red.off()
        led_encendido = False
       
    else:
        red.on()
        led_encendido = True
        
def apagar_rap():
    # Lógica para apagar la Raspberry Pi
    check_call(['sudo', 'poweroff'])

def contar_tiempo():
    global contador_activo, tiempo
    while True:
        if contador_activo:
            if tiempo <= 0:
                contador_activo = False
                tiempo = 0
                orange.off()
            else:
                tiempo -= 1
                orange.on()
        else:
            orange.off()
        time.sleep(1)

def actualizar_sensor_hum(datos):
    while True:
        hum, temp = sensor_humytemp()
        datos[1] = '{0:0.1f} C '.format(temp)
        datos[2] = '{0:0.1f} %'.format(hum)
        time.sleep(0.1)

def actualizar_nivel_agua(datos):
    while True:
        if not GPIO.input(pin_agua):
            white.on()
            datos[3] = "Necesito agua"
        else:
            white.off()
            datos[3] = "Estoy Lleno"
        time.sleep(0.1)
        
def data_received(received_data):
    global led_encendido, contador_activo, tiempo
    data = received_data
    print(data)
    if data == 'L':
        red.on()
        led_encendido = True
    elif data == 'Y':
        red.off()
        led_encendido = False
    elif data == 'H':
        boton_huminificador()
    elif data == 'R':
        boton_reinicio()
    elif data == 'P':
        apagar_rap()
        
def main():
    datos = ["","", "", "", "",""]
    server = BluetoothServer(data_received)
    boton_apagar_rap = Button(btn_apagar_raspi, hold_time=3)
    boton_apagar_rap.when_held = apagar_rap
    btn_humi.when_pressed = boton_huminificador
    shutdown_btn = Button(btn_reset, hold_time=2)
    shutdown_btn.when_held = boton_reinicio
    GPIO.setup(pin_agua, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(btn_leds, GPIO.BOTH, callback=boton_leds_apagar_y_prender, bouncetime=200)

    hilo_sensor_hum = threading.Thread(target=actualizar_sensor_hum, args=(datos,))
    hilo_tiempo = threading.Thread(target=contar_tiempo)
    hilo_nivel_agua = threading.Thread(target=actualizar_nivel_agua, args=(datos,))

    hilo_sensor_hum.start()
    hilo_tiempo.start()
    hilo_nivel_agua.start()

    while True:
        datos[4] = mostrar_tiempo()
        datos[5] = "Encendidos" if led_encendido else "Apagados"
        print("{}".format(" / ".join(datos)))
        server.send("{}".format(" / ".join(datos)))
        time.sleep(0.01)

if __name__ == "__main__":
    main()