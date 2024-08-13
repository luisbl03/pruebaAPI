from pymongo import MongoClient

#base de datos local
#dbclient = MongoClient().local

#base de datos en la nube
dbclient = MongoClient("mongodb+srv://darkterminator03:fiestapagana2003@cluster0.wpke4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test