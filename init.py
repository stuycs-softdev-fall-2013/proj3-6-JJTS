import json, urllib, urllib2
from pymongo import MongoClient
import utils

client = MongoClient()
db = client.pcparts

url = "http://www.ows.newegg.com/Stores.egg/Categories/1"


resp = urllib2.urlopen(url)
data = json.loads(resp.read())
cases = data[4]
cpus = data[5]
hdds = data[8]
ram = data[11]
mobos = data[13]
psus = data[16]
ssds = data[22]
gpus = data[23]
group = [cases,cpus,hdds,ram,mobos,psus,ssds,gpus]
names = ["cases","cpus","hdds","ram","mobos","psus","ssds","gpus"]


def check(string):
    return ((not("Open Box" in string)) and (not("Refurbished" in string)) and (not("ELEC" in string)) and (not("Laiputuo" in string)))

def init(group, names,something,i):
    catID = str(group["CategoryID"])
    nodID = str(group["NodeId"])
    
    url = "http://www.ows.newegg.com/Stores.egg/Navigation/1/{Cat}/{Node}"
    url1 = url.replace("{Cat}", catID)
    url2 = url1.replace("{Node}", nodID)
    resp = urllib2.urlopen(url2)
    data = json.loads(resp.read())
        #data[1] for motherboards to account for intel and amd
    subcatID = data[something]["CategoryID"]
    nodeID = data[something]["NodeId"]
    
    
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
    count = 0
    asdf = data["ProductListItems"]
    
    
    while (count < 20):
        final = asdf[count]
        addstuff = dict()
        addstuff["Title"] = final["Title"].encode("ascii","ignore")
        addstuff["fPrice"] = final["FinalPrice"].encode("ascii","ignore")
        addstuff["oPrice"] = final["OriginalPrice"].encode("ascii","ignore")
        addstuff["Model"] = final["Model"].encode("ascii","ignore")
        addstuff["ItemNumber"] = final["ItemNumber"].encode("ascii","ignore")
        addstuff["Newegg"] = final["NeweggItemNumber"].encode("ascii","ignore")
        addstuff["Rating"] = final["ReviewSummary"]["Rating"]
        addstuff["numRating"] = final["ReviewSummary"]["TotalReviews"].encode("ascii","ignore")
        #url5 = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", addstuff["ItemNumber"])
        #response1 = urllib2.urlopen(url5)
        #thingy = json.loads(response1.read())
        if (check(addstuff["Title"])):
             if(i == 0):
                 specs = utils.getCaseSpecs(addstuff['ItemNumber'])
                 db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
             if(i == 1):
                 specs = utils.getCPUSpecs(addstuff['ItemNumber'])
                 db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
             if(i == 2):
                 specs = utils.getHDDSpecs(addstuff['ItemNumber'])
                 db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
             if(i == 3):
                 specs = utils.getRAMSpecs(addstuff['ItemNumber'])
                 db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
             if(i == 4):
                 specs = utils.getMoboSpecs(addstuff['ItemNumber'])
                 db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
             if(i == 5):
                 specs = utils.getPSUSpecs(addstuff['ItemNumber'])
                 db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
             if(i == 6):
                 specs = utils.getSSDSpecs(addstuff['ItemNumber'])
                 db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
             if(i == 7):
                 specs = utils.getGPUSpecs(addstuff['ItemNumber'])
                 db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
             print(addstuff["Title"])
        count = count + 1
        
#url = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", addstuff["ItemNumber"])
#response = urllib2.urlopen(request)
#data = json.loads(response.read())
#print data
        
#print data["ProductListItems"][0]
    total = data["PaginationInfo"]["TotalCount"]
        
    pagenum = 2
    while (pagenum * 20 < total):
        data = {
            "SubCategoryId": subcatID,
            "NValue": "",
            "StoreDepaId": 1,
            "NodeId": nodeID,
            "BrandId": -1,
            "PageNumber": pagenum,
            "CategoryId": catID
            }
        
        url = "http://www.ows.newegg.com/Search.egg/Advanced"
        params = json.dumps(data).replace("null","-1")
        request = urllib2.Request(url, params)
        response = urllib2.urlopen(request)
        data = json.loads(response.read())
        count = 0
        asdf = data["ProductListItems"]
        
        
        while (count < 20):
            final = asdf[count]
            addstuff = dict()
            addstuff["Title"] = final["Title"].encode("ascii","ignore")
            addstuff["fPrice"] = final["FinalPrice"].encode("ascii","ignore")
            addstuff["oPrice"] = final["OriginalPrice"].encode("ascii","ignore")
            addstuff["Model"] = final["Model"].encode("ascii","ignore")
            addstuff["ItemNumber"] = final["ItemNumber"].encode("ascii","ignore")
            addstuff["Newegg"] = final["NeweggItemNumber"].encode("ascii","ignore")
            addstuff["Rating"] = final["ReviewSummary"]["Rating"]
            addstuff["numRating"] = final["ReviewSummary"]["TotalReviews"].encode("ascii","ignore")
            #url5 = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", addstuff["ItemNumber"])
            #response1 = urllib2.urlopen(url5)
            #thingy = json.loads(response1.read())
            if (check(addstuff["Title"])):
                if(i == 0):
                    specs = utils.getCaseSpecs(addstuff['ItemNumber'])
                    db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
                if(i == 1):
                    specs = utils.getCPUSpecs(addstuff['ItemNumber'])
                    db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
                if(i == 2):
                    specs = utils.getHDDSpecs(addstuff['ItemNumber'])
                    db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
                if(i == 3):
                    specs = utils.getRAMSpecs(addstuff['ItemNumber'])
                    db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
                if(i == 4):
                    specs = utils.getMoboSpecs(addstuff['ItemNumber'])
                    db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
                if(i == 5):
                    specs = utils.getPSUSpecs(addstuff['ItemNumber'])
                    db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
                if(i == 6):
                    specs = utils.getSSDSpecs(addstuff['ItemNumber'])
                    db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
                if(i == 7):
                    specs = utils.getGPUSpecs(addstuff['ItemNumber'])
                    db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs})
                print(addstuff["Title"])
            count = count + 1
                
        pagenum = pagenum + 1
                
        
i = 0
while (i < 8):
    init(group[i], names, 0,i)
    i = i + 1
init(mobos, "mobos", 1,4)
