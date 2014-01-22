import json, urllib, urllib2
from pymongo import MongoClient

client = MongoClient()
db = client.pcparts

#go to http://www.ows.newegg.com/Products.egg/11-235-038/Specification

def getSpecs(itemnum):
    url = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", itemnum)
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    return data["SpecificationGroupList"]


