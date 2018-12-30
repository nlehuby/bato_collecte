# encoding: utf-8
import csv
import subprocess

#on écrase le fichier précédemment créé
fieldnames = ['source','stop_id','latitude','longitude','stop_name','transport_mode']
outfile = 'resultats/BATO_GTFS.csv'
with open(outfile, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

#on lit le fichier csv contenant les liens de téléchargements des GTFS
with open('sources_GTFS.csv', 'r') as f:
    dictReader = csv.DictReader(f)
    for a_GTFS in dictReader:

        print(a_GTFS['Description'])

        #on télécharge le GTFS
        subprocess.call(['wget', '-nv', '--output-document=GTFS.zip', a_GTFS['Download']])

        #on extrait le GTFS
        subprocess.call(['unzip', 'GTFS.zip', '-d', 'temp'])

        #on crée un fichier pour décrire la source
        with open('temp/temp_stop_source.csv', 'w') as sourcefile:
            writer = csv.DictWriter(sourcefile, fieldnames=['source'])
            writer.writeheader()
            writer.writerow({'source': "opendata_GTFS_" + a_GTFS['ID']})

        #on extrait les arrêts
        subprocess.call(['./extract_stops_from_GTFS.sh'])

        #on supprime les fichiers temporaires
        subprocess.call(['rm', 'GTFS.zip'])
        subprocess.call(['rm', '-r', 'temp'])
