#!/usr/bin/env python3 
#-----------------------------------------------------------------------------------------------
# Garmin FIT to GeoJSON Converter
#-----------------------------------------------------------------------------------------------
#
# Description:
#   Converts `Lctns.fit` to GeoJSON from a Garmin Instinct or similar watch.
#
#   Arran Smith
#   Created: 2020-08-19
#
#-----------------------------------------------------------------------------------------------

import sys
import argparse
import fitparse
from geojson import Point, Feature, FeatureCollection, dumps

# Convert FIT to GeoJSON
class FitGeoJSONConverter:

    def __init__(self):
        self.location_message = "unknown_29"
        self.field_mapping = {
            "name": "unknown_0",
            "id": "unknown_254",
            "longitude": "unknown_2",
            "latitude": "unknown_1",
            "icon": "unknown_4",
        }
    
    def convert(self, filename):

        # Load the FIT file

        # https://pythonhosted.org/fitparse/api.html
        fitfile = fitparse.FitFile(filename)

        # Iterate over all messages of type "record"
        # (other types include "device_info", "file_creator", "event", etc)
        fit_messages = []
        for record in fitfile.get_messages(self.location_message):

            fit_message = {}
            # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
            for data in record:
            
                # Skip empty data
                if data.value is None:
                    continue

                for key, value in self.field_mapping.items():
                    if data.name == value:
                        if data.name == self.field_mapping["longitude"] or data.name == self.field_mapping["latitude"]:
                            # Garmin saves the position as a 32Bit Signed Int
                            # https://gis.stackexchange.com/questions/371656/garmin-fit-coodinate-system/371667#371667

                            fit_message[key] = data.value / (2**32 / 360)
                        else:
                            fit_message[key] = data.value
            
            fit_messages.append(fit_message)

        # Create GeoJson Features
        features = []
        for fit_message in fit_messages:
            point = Point((fit_message["longitude"], fit_message["latitude"]))
            props = {key:val for key, val in fit_message.items() if key != "longitude" and key != "latitude"} 
            feature = Feature(geometry=point, properties=props)
            features.append(feature)

        return FeatureCollection(features)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("fit_geojson_conveter", description='Convert FIT to GeoJSON')
    parser.add_argument("-i", "--input", help="FIT input file location", type=str, required=True)
    parser.add_argument("-o", "--output", help="GeoJSON output file location", type=str, required=False)
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    geoJSON = converter = FitGeoJSONConverter().convert(args.input)

    if args.output:
        file = open(args.output, "w")
        file.write(dumps(geoJSON))
        file.close()

    else:
        print(geoJSON)
