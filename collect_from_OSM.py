#!/usr/bin/env python
# coding: utf-8

import osmium
import csv

class BATOHandler(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.stops = []

    def node(self, n):
        elem = {}

        if  ('highway' in n.tags and n.tags['highway'] == 'bus_stop')  :
            elem['stop_id'] = n.id
            elem['transport_mode'] = "bus"

        elif ('amenity' in n.tags and n.tags['amenity'] == 'ferry_terminal') :
            elem['stop_id'] = n.id
            elem['transport_mode'] = "bateau"

        elif  ('aerialway' in n.tags and n.tags['aerialway'] == 'station')  :
            elem['stop_id'] = n.id
            elem['transport_mode'] = "cable"

        elif ('railway' in n.tags and n.tags['railway'] in ('station', 'halt', 'tram_stop')) :
            elem['stop_id'] = n.id
            transport_mode = "train"
            if n.tags['railway'] == 'tram_stop':
                transport_mode = "tramway"
            if 'station' in n.tags and n.tags['station'] == "subway":
                transport_mode = "métro"
            elem['transport_mode'] = transport_mode

        if 'stop_id' in elem:
            elem['latitude'] = n.location.lat
            elem['longitude'] = n.location.lon
            elem['source'] = "OpenStreetMap"
            elem['stop_name'] = ''
            if 'name' in n.tags :
                elem['stop_name'] = n.tags['name']
            self.stops.append(elem)

osm_history_file = "data.osm.pbf"

bato_handler = BATOHandler()
bato_handler.apply_file(osm_history_file)
bato_handler.stops

fieldnames = ['source','stop_id','latitude','longitude','stop_name','transport_mode']

outfile = 'resultats/BATO_OSM.csv'
with open(outfile, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    for a_row in bato_handler.stops:
        writer.writerow(a_row)
