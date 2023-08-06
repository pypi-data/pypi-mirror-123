# NotecardPseudoSensor

NotecardPseudoSensor provides an API interface to the internal sensors of the [Blues Wireless Notecard](https://shop.blues.io/collections/notecard). The goal of this abstraction is to offer a sensor to use with more advanced tutorials, which enables focus on the syntax necessary to perform basic Notecard transactions for those new to the platform.

## Installation

With `pip` via PyPi:

```
pip install notecard-pseudo-sensor
```

or

```
pip3 install notecard-pseudo-sensor
```


## Usage

``` python
import notecard-pseudo-sensor

sensor = notecard-pseudo-sensor.NotecardPseudoSensor()
print(sensor.temp())
print(sensor.humidity())
```

## To learn more about Blues Wireless, the Notecard and Notehub, see:

- [blues.io](https://blues.io)
- [notehub.io](https://notehub.io)
- [dev.blues.io](https://dev.blues.io)

## License

Copyright (c) 2021 Blues, Inc. Released under the MIT license. See
[LICENSE](LICENSE.mit) for details.