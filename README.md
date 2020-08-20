# FitGeoJSON Converter

Watches such as the Garmin Instinct store saved locations in a `FIT` file called `Lctns.fit`, However this file is 
treated differently to other `FIT` files on the device - So processing with other FIT utilities is not possible.

This python script **ONLY** converts `Lctns.fit` from a Garmin watch into GeoJSON.

## Requirements

- [geojson](https://github.com/jazzband/geojson)
- [fitparse](https://github.com/dtcooper/python-fitparse)


## Usage

```
usage: fit_geojson_conveter [-h] -i INPUT [-o OUTPUT]

Convert FIT to GeoJSON

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        FIT input file location
  -o OUTPUT, --output OUTPUT
                        GeoJSON output file location
```


