#!/bin/bash
cd ./temp

echo "##### on filtre les stop_times #####"
cat stop_times.txt |xsv select stop_id,trip_id > temp_stop_times_light.csv

echo "##### on récupère les codes de lignes #####"
xsv join trip_id temp_stop_times_light.csv trip_id trips.txt |xsv select stop_id,route_id|xsv sort|uniq > temp_stop_with_routes.csv

echo "##### on récupère le mode de la ligne #####"
xsv join route_id temp_stop_with_routes.csv route_id routes.txt |xsv select stop_id,route_type|xsv sort|uniq > temp_stop_with_mode.csv

echo "##### on récupère les infos de l'arrêt #####"
xsv join stop_id stops.txt stop_id temp_stop_with_mode.csv |xsv select 'stop_id[0],stop_lat,stop_lon,stop_name,route_type' > temp_stop_full.csv

echo "##### on ajoute la colonne source #####"
xsv join --cross source temp_stop_source.csv stop_id temp_stop_full.csv > temp_stop_gtfs.csv

echo "##### on renomme pour éviter les doublons de colonnes #####"
echo "source,stop_id,latitude,longitude,stop_name,transport_mode" > stops_gtfs.csv
tail -n +2 temp_stop_gtfs.csv >> stops_gtfs.csv

echo "##### on ajoute au fichier global#####"
tail -n +2 stops_gtfs.csv >> ../resultats/BATO_GTFS.csv
