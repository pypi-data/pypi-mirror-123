# MATMOS

![alt text](tests/coverage/coverage.svg ".coverage available in tests/coverage/")

MATMOS is a direct and inverse atmospheric model library. Currently it supports 
the International Standard Atmosphere model.

## Install

`pip install matmos`

## User's guide

Given an altitude, MATMOS allows you to calculate the temperature, pressure and 
density of the atmosphere (direct model). If given any of these (temperature,
pressure or density), MATMOS will calculate the corresponding altitude and remaining 
quantities (indirect model).

As temperature is not a monotonic function of altitude (equal values of temperature happen 
at different altitudes), its inverse cannot be determined without more information. To solve 
this, the option to specify an altitude range where the temperature is to be found is 
provided.

[The API reference is available here](https://alopezrivera-docs.github.io/matmos/).

## Install

`pip install matmos`

## Models

### ISA

![alt text](demo/graphs/ISA.png)

## User's guide
 
### Importing a model

```
from matmos import ISA
```

### Running and retrieving results

The model is run by simply initializing an instance with 
height, temperature, pressure or density as inputs. 
The results are stored as instance attributes and can be retrieved with
the usual notation.

MATMOS allows for input in the form of Python numeric types as well as NumPy arrays. 
The unit convention can be seen in the table below.

| Magnitude | Altitude | Temperature | Pressure | Density | 
| ---       | ---      | ---         | ---      | ---     | 
| Unit      | km       | K           | Pa       | kg/m^3  |

#### Direct model

Solving for a given height:

```
m = ISA(23.5)                       # 23.5 km

m.t                                 # Temperature
m.p                                 # Pressure
m.d                                 # Density
```

#### Inverse model

Solving for a given temperature:

```
m = ISA(t=225, hrange=[0, 20])      # 225 K, in the range from 0 to 20 km

m.h                                 # Altitude
m.t                                 # Temperature
m.d                                 # Density
```

Solving for a given pressure:

```
m = ISA(p=98000)                    # 98000 Pa

m.h                                 # Altitude
m.t                                 # Temperature
m.d                                 # Density
```

Solving for a given density:

```
m = ISA(p=0.03)                     # 0.03 kg/m^3

m.h                                 # Altitude
m.t                                 # Temperature
m.p                                 # Pressure
```

---
[Back to top](#matmos)
