import json, urllib, urllib2

url = "http://www.ows.newegg.com/Stores.egg/Categories/1"


resp = urllib2.urlopen(url)
data = json.loads(resp.read())
cases = data[4]
catID = str(cases["CategoryID"])
nodID = str(cases["NodeId"])

url = "http://www.ows.newegg.com/Stores.egg/Navigation/1/{Cat}/{Node}"
url1 = url.replace("{Cat}", catID)
url2 = url1.replace("{Node}", nodID)
resp = urllib2.urlopen(url2)
data = json.loads(resp.read())
subcatID = data[0]["CategoryID"]
nodeID = data[0]["NodeId"]

data = {
    "SubCategoryId": subcatID, 
    "NValue": "", 
    "StoreDepaId": 1, 
    "NodeId": nodeID, 
    "BrandId": -1, 
    "PageNumber": 1, 
    "CategoryId": catID
}

url = "http://www.ows.newegg.com/Search.egg/Advanced"
params = json.dumps(data).replace("null","-1")
request = urllib2.Request(url, params)
response = urllib2.urlopen(request)
data = json.loads(response.read())

print data["ProductListItems"][0]["Title"]
