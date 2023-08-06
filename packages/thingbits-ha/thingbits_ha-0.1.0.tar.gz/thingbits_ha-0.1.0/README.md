# ThingBits Home Assistant Integration
```python3
from thingbits_ha import discover
from asyncio import run

run(discover())
```

## APIs
 - `async def discover()`: Asynchronous function that checks the network
   for new devices and returns them in a list.
