Deploy with dokku

Need storage
link all_stations_data.pkl file (from the location it is updated using get_data_python) to /var/lib/dokku/data/storage/<appname>
then 
dokku storage:mount mvmon /var/lib/dokku/data/storage/mvmon:/app/data

