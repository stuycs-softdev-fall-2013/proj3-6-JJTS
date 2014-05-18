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
    string = string.lower()
    list = ["asus", "ddr3", "intel", "crucial", "wd", "western digital", "seagate", "corsair", "gigabyte", "msi",
            "g.skill", "samsung", "ocz", "plextor", "antec", "cooler master", "nzxt", "fractal design", "cougar", "thermaltake",
            "rosewill", "asrock", "radeon r9", "gtx 6", "radeon hd 78", "be quiet", "seasonic", "amd"]
    if ("open box" in string or "refurbished" in string):
        return False
    bad = ["ecs", "supermicro", "avatar", "biostar", "five star inc", "foxconn", "jetway", "l337"]
    for x in bad:
        if x in string:
            return False
    for x in list:
        if x in string:
            return True
    return False
    
    #more exceptions

def thing(addstuff, i):
    if(i == 0):
        reviews = utils.getReviews(addstuff['ItemNumber'])
        specs = utils.getCaseSpecs(addstuff['ItemNumber'])
        db.cases.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs, 'reviews':reviews})
        
    if(i == 1):
        reviews = utils.getReviews(addstuff['ItemNumber'])
        specs = utils.getCPUSpecs(addstuff['ItemNumber'])
        db.cpus.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs, 'reviews':reviews})
        
    if(i == 2):
        reviews = utils.getReviews(addstuff['ItemNumber'])
        specs = utils.getHDDSpecs(addstuff['ItemNumber'])
        db.hdds.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs, 'reviews':reviews})
        
    if(i == 3):
        reviews = utils.getReviews(addstuff['ItemNumber'])
        specs = utils.getRAMSpecs(addstuff['ItemNumber'])
        db.ram.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs, 'reviews':reviews})

    if(i == 4):
        reviews = utils.getReviews(addstuff['ItemNumber'])
        specs = utils.getMoboSpecs(addstuff['ItemNumber'])
        db.mobos.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs, 'reviews':reviews})
        
    if(i == 5):
        reviews = utils.getReviews(addstuff['ItemNumber'])
        specs = utils.getPSUSpecs(addstuff['ItemNumber'])
        db.psus.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs, 'reviews':reviews})
            
    if(i == 6):
        reviews = utils.getReviews(addstuff['ItemNumber'])
        specs = utils.getSSDSpecs(addstuff['ItemNumber'])
        db.ssds.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs, 'reviews':reviews})

    if(i == 7):
        reviews = utils.getReviews(addstuff['ItemNumber'])
        specs = utils.getGPUSpecs(addstuff['ItemNumber'])
        db.gpus.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs, 'reviews':reviews})

    db.parts.insert({'itemnumber':addstuff['ItemNumber'], 'stuff':addstuff, 'specs':specs, 'reviews':reviews})

    print(addstuff["Title"])

def init(group, names,something,thingy):
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
        addstuff["fPrice"] = final["FinalPrice"].encode("ascii","ignore").replace(",","")
        addstuff["oPrice"] = final["OriginalPrice"].encode("ascii","ignore").replace(",","")
        addstuff["Model"] = final["Model"].encode("ascii","ignore")
        addstuff["ItemNumber"] = final["ItemNumber"].encode("ascii","ignore")
        addstuff["Newegg"] = final["NeweggItemNumber"].encode("ascii","ignore")
        addstuff["Rating"] = final["ReviewSummary"]["Rating"]
        addstuff["numRating"] = final["ReviewSummary"]["TotalReviews"].encode("ascii","ignore")
        #url5 = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", addstuff["ItemNumber"])
        #response1 = urllib2.urlopen(url5)
        #thingy = json.loads(response1.read())
        if (check(addstuff["Title"])):
            thing(addstuff,thingy)
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
            addstuff["fPrice"] = final["FinalPrice"].encode("ascii","ignore").replace(",","")
            addstuff["oPrice"] = final["OriginalPrice"].encode("ascii","ignore").replace(",","")
            addstuff["Model"] = final["Model"].encode("ascii","ignore")
            addstuff["ItemNumber"] = final["ItemNumber"].encode("ascii","ignore")
            addstuff["Newegg"] = final["NeweggItemNumber"].encode("ascii","ignore")
            addstuff["Rating"] = final["ReviewSummary"]["Rating"]
            addstuff["numRating"] = final["ReviewSummary"]["TotalReviews"].encode("ascii","ignore")
            #url5 = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", addstuff["ItemNumber"])
            #response1 = urllib2.urlopen(url5)
            #thingy = json.loads(response1.read())
            if (check(addstuff["Title"])):
                thing(addstuff,thingy)
            count = count + 1
                
        pagenum = pagenum + 1
                
        
i = 3
while (i < 8):
    init(group[i], names, 0,i)
    i = i + 1
#init(mobos, "mobos", 1,4)
