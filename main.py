from decouple import config
from read_wavemini import WaveMini
import signal
import sys
import time
import requests

WAVE_SERIAL_NUMBER = config('SERIAL_NUMBER')
WAVE_SAMPLE_PERIOD = config('SAMPLE_PERIOD')

def send_values(temperature, humidity, voc):
    #result = requests.get('https://w3schools.com/python/demopage.htm')
    msg = "Temperature: {} *C, ".format(temperature)
    msg += "Humidity: {} %rH, ".format(humidity)
    msg += "VOC: {} ppm".format(voc)
    print(msg)


def _main():
    wavemini = WaveMini(WAVE_SERIAL_NUMBER)

    def _signal_handler(sig, frame):
        wavemini.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT, _signal_handler)

    while True:
        wavemini.connect(retries=3)
        current_values = wavemini.read()
        send_values(current_values.temperature, current_values.humidity, current_values.voc)
        wavemini.disconnect()
        time.sleep(WAVE_SAMPLE_PERIOD)

if __name__ == "__main__":
    _main()
