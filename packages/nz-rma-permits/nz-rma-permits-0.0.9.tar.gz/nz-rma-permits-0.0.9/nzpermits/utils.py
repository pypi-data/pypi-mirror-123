#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:18:45 2021

@author: mike
"""
import orjson
from geojson import Point
from hashlib import blake2b

###################################################
### Functions


def create_geometry(coords, geo_type='Point'):
    """

    """
    if geo_type == 'Point':
        coords = [round(coords[0], 5), round(coords[1], 5)]
        geo1 = Point(coords)
    else:
        raise ValueError('geo_type not implemented yet')

    if not geo1.is_valid:
        raise ValueError('coordinates are not valid')

    geo2 = dict(geo1)

    return geo2


def assign_station_id(geometry):
    """

    """
    station_id = blake2b(orjson.dumps(geometry, option=orjson.OPT_SERIALIZE_NUMPY), digest_size=12).hexdigest()

    return station_id
