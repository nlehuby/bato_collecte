# encoding: utf-8
import csv
import requests

def get_gtfs_list_from_transport_datagouv_api():
    import json

    url = 'https://transport.data.gouv.fr/api/datasets'
    resp = requests.get(url)

    gtfs_sources = []
    for dataset in resp.json():
        for resource in dataset['resources']:
            gtfs = {}
            gtfs["ID"] = dataset.get('datagouv_id', None)
            gtfs["Licence"] = ""
            gtfs["Source link"] = resource.get('url', None)
            gtfs["Description"] = dataset['title'] + resource.get('title', None)
            gtfs["Download"] = resource.get('url', None)

            gtfs_sources.append(gtfs)
    return gtfs_sources

def get_gtfs_list_from_transport_datagouv_rss_feed():
    import xml.etree.ElementTree as ET
    url = 'https://transport.data.gouv.fr/atom.xml'
    resp = requests.get(url)
    root = ET.fromstring(resp.content)

    gtfs_sources = []

    for a_gtfs in root.findall('{http://www.w3.org/2005/Atom}entry'):
        gtfs = {}
        gtfs["ID"] = a_gtfs.find('{http://www.w3.org/2005/Atom}id').text.split('/')[-1]
        gtfs["Licence"] = ""
        gtfs["Source link"] = a_gtfs.find('{http://www.w3.org/2005/Atom}id').text
        gtfs["Description"] = a_gtfs.find('{http://www.w3.org/2005/Atom}title').text
        gtfs["Download"] = a_gtfs.find('{http://www.w3.org/2005/Atom}link').attrib['href']

        gtfs_sources.append(gtfs)
    return gtfs_sources

def get_gtfs_list_from_navitia_io():
    navitiaio_sources = [
        "https://navitia.opendatasoft.com/explore/dataset/fr-se/download/?format=json&timezone=Europe/Berlin",
        "https://navitia.opendatasoft.com/explore/dataset/fr-sw/download/?format=json&timezone=Europe/Berlin",
        "https://navitia.opendatasoft.com/explore/dataset/fr-ne/download/?format=json&timezone=Europe/Berlin",
        "https://navitia.opendatasoft.com/explore/dataset/fr-nw/download/?format=json&timezone=Europe/Berlin"
    ]

    gtfs_sources = []
    for source in navitiaio_sources:
        json_list = requests.get(source).json()
        for dataset in json_list:
            #if dataset['fields']['type_file'] != "provider" : continue
            if dataset['fields']['format'] != "GTFS" : continue
            gtfs = {}
            gtfs["ID"] = dataset['fields']["id"]
            gtfs["Licence"] = dataset['fields'].get("licence", None)
            gtfs["Source link"] = dataset['fields'].get("source_link", None)
            gtfs["Description"] = dataset['fields'].get("description", None)
            gtfs["Download"] = "https://navitia.opendatasoft.com/api/datasets/1.0/{}/images/{}".format(
                dataset["datasetid"],
                dataset["fields"]["download"]["id"]
            )
            gtfs_sources.append(gtfs)
    # on ajoute le jeu de données du STIF :
    gtfs = {}
    gtfs["ID"] = "fr-idf-OIF"
    gtfs["Licence"] = "ODbL"
    gtfs["Source link"] = "http://opendata.stif.info/explore"
    gtfs["Description"] = "Transport in Paris and Suburb"
    gtfs["Download"] = "https://navitia.opendatasoft.com/api/datasets/1.0/fr-idf/images/14bd1111dd3d3e845924bb0876e175b1"
    gtfs_sources.append(gtfs)

    return gtfs_sources


gtfs_sources = get_gtfs_list_from_navitia_io()

fieldnames = ["ID", "Licence", "Source link", "Description", "Download"]
with open("sources_GTFS.csv", 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for g in gtfs_sources:
        writer.writerow(g)
