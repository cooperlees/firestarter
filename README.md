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
* J1 to RaspberryPi expansion header
* J2 to existing control wires
* J3 to existing manual switch
