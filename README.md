# What is it

A small python utility I use to monitor the health of my accumulators using [Reload: Pro](http://www.arachnidlabs.com/reload-pro/)

It uses [rlpro-ppython](https://github.com/arachnidlabs/rlpro-python/) and [matplotlib](https://matplotlib.org/).

source code is based on https://matplotlib.org/gallery/animation/animate_decay.html#sphx-glr-gallery-animation-animate-decay-py
and https://github.com/arachnidlabs/rlpro-python/blob/master/rlpro/characterize.py.

# Usage

```
python ./accu_discharge.py --help               
usage: accu_discharge.py [-h] [--current AMPS] [--delay SECONDS]
                         [--baudrate BAUD] [--timeout SECS]
                         [--min_voltage VOLTS] [--file FILE]
                         PORT

Evaluate capacity of an accumulator

positional arguments:
  PORT                 Serial port to use

optional arguments:
  -h, --help           show this help message and exit
  --current AMPS       Current to test with
  --delay SECONDS      Interval between measurements
  --baudrate BAUD      Baud rate to use when flashing using serial (default
                       115200)
  --timeout SECS       Time to wait for a Bootloader response (default 5)
  --min_voltage VOLTS  Minimum voltage to reach
  --file FILE          CSV file to create
```

Example:
`python ./accu_discharge.py --delay 60 --current .2 --min_voltage 3 /dev/tty.usbserial-DAXWP1ZJ`
will take a measure point every 60s at a fixed current of .2 amps, and stop when the voltage goes at or under 3V.

