# Tenma 72-13210 DC load library

A simple library to contol the Tenma 72-13210

```python
from tenma_dc_load import DCload

dc = DCload("COM8")

dc.set_power(10) # request a 10W draw 
dc.turn_on()

while True:
    print(dc.get_current())
```