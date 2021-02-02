from decouple import config
from read_wavemini import WaveMini
import signal
import sys
import time

WAVE_SERIAL_NUMBER = config('SERIAL_NUMBER')
WAVE_SAMPLE_PERIOD = config('SAMPLE_PERIOD')

def _main():
    wavemini = WaveMini(WAVE_SERIAL_NUMBER)

    def _signal_handler(sig, frame):
        wavemini.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT, _signal_handler)

    while True:
        wavemini.connect(retries=3)
        current_values = wavemini.read()
        print(current_values)
        wavemini.disconnect()
        time.sleep(WAVE_SAMPLE_PERIOD)

if __name__ == "__main__":
    _main()
