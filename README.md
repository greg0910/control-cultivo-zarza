# Sistema de Monitoreo y Control de Humedad y LEDs con Bluetooth

Este proyecto permite monitorear la humedad, controlar LEDs y gestionar un humidificador mediante una conexión Bluetooth utilizando una Raspberry Pi.

## Requisitos

- Raspberry Pi con conexión a internet
- Sensor DHT11 conectado al pin GPIO 18
- LED rojo conectado al pin GPIO 23
- LED blanco conectado al pin GPIO 20
- LED naranja conectado al pin GPIO 21
- Botón de encendido y apagado de LEDs en el pin GPIO 22
- Botón de humidificador en el pin GPIO 17
- Botón de reinicio en el pin GPIO 24
- Botón de apagado de Raspberry Pi en el pin GPIO 27
- Pin de control de nivel de agua en el pin GPIO 25
- Dispositivo móvil con sistema operativo Android y la aplicación MIT App Inventor Bluetooth Client instalada

## Instalación

1. Asegúrate de tener Python 3 y las librerías `Adafruit_DHT`, `gpiozero`, `RPi.GPIO`, `bluedot` y `time` instaladas en tu Raspberry Pi.
2. Descarga el código en un archivo `.py` en tu Raspberry Pi.
3. Ejecuta el código con el comando `python nombre_del_archivo.py` en la terminal.
4. En tu dispositivo móvil, abre la aplicación MIT App Inventor Bluetooth Client y conéctate al servidor Bluetooth de tu Raspberry Pi.

## Uso

### Botones Físicos

- **Botón de Humidificador (GPIO 17):** Inicia el humidificador por 5 minutos. Si se presiona nuevamente, extiende el tiempo en incrementos de 5 minutos.
- **Botón de Reinicio (GPIO 24):** Reinicia el temporizador del humidificador a cero.
- **Botón de LEDs (GPIO 22):** Enciende o apaga el LED rojo.
- **Botón de Apagado de Raspberry Pi (GPIO 27):** Mantén presionado por 3 segundos para apagar la Raspberry Pi.

### Uso del Dispositivo Móvil

Utilizando la aplicación MIT App Inventor Bluetooth Client, puedes enviar los siguientes comandos para interactuar con el sistema:

- `L`: Encender el LED rojo
- `Y`: Apagar el LED rojo
- `H`: Iniciar el humidificador por 5 minutos (se puede extender el tiempo en incrementos de 5 minutos)
- `R`: Reiniciar el tiempo del humidificador
- `P`: Apagar la Raspberry Pi

## Funcionalidades Adicionales

- **Sensor de Humedad y Temperatura:** El sistema monitorea continuamente la humedad y la temperatura utilizando un sensor DHT11, y los datos se actualizan en tiempo real.
- **Control de LEDs:** Los LEDs rojo, blanco y naranja pueden ser controlados manualmente mediante botones físicos o comandos Bluetooth.
- **Nivel de Agua:** El sistema verifica el nivel de agua y enciende el LED blanco si es necesario rellenar el agua.
- **Temporizador de Humidificador:** Un temporizador controlado por un botón físico o comando Bluetooth gestiona el tiempo de funcionamiento del humidificador.

## Notas

- Asegúrate de tener los pines de los componentes conectados correctamente según el código, de lo contrario, no funcionarán correctamente.
- El botón de apagado de la Raspberry Pi requiere mantener presionado por 3 segundos para ejecutar el comando de apagado.
