# firestarter

Web Interface to start and stop my fireplace.

## Manual sys 'API'

### Setup Pins

```shell
echo "2" > /sys/class/gpio/export
echo "3" > /sys/class/gpio/export
echo "in" > /sys/class/gpio/gpio3/direction
echo "out" > /sys/class/gpio/gpio2/direction && echo "1" > /sys/class/gpio/gpio2/value
```

### Get State

```
cat /sys/class/gpio/gpio3/value
```

### Change State

```shell
echo "0" > /sys/class/gpio/gpio2/value && sleep 0.1 && echo "1" > /sys/class/gpio/gpio2/value
```

### Default State

```shell
echo "2" > /sys/class/gpio/unexport
echo "3" > /sys/class/gpio/unexport
```

### RaspberryPi firestarter HAT Schematic

![firestarter HAT](https://github.com/cooperlees/firestarter/blob/main/firestarter_hat.png)

- J1 to RaspberryPi expansion header
- J2 to existing control wires
- J3 to existing manual switch

## Docker

Docker build works and defaults to two workers with gunicorn.

- `docker build -t firestarter .`

## Development

Install all into a virtualenv and start like any other gunicorn aiohttp web application.

- uvloop is default but optional ...

```sh
sudo apt install python3-rpi.gpio
python3 -m venv --system-site-packages /tmp/tbf/
/tmp/tbf/bin/pip install --upgrade pip setuptools
/tmp/tbf/bin/pip install -e .
/tmp/tbf/bin/gunicorn --bind=[::]:1469 --access-logfile=- --name=firestarter \
    --workers=2 --worker-class=aiohttp.worker.GunicornUVLoopWebWorker "firestarter.server:serve"
```
