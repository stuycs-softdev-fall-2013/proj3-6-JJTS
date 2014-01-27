import json, urllib, urllib2
from pymongo import MongoClient

client = MongoClient()
db = client.pcparts

#go to http://www.ows.newegg.com/Products.egg/11-235-038/Specification

def getCaseSpecs(itemnum):
    url = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", itemnum)
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    model = dict()
    specs = dict()
    expan = dict()
    front = dict()
    data = data["SpecificationGroupList"]
    try:
        for x in data[0]["SpecificationPairList"]:
            model[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[1]["SpecificationPairList"]:
            specs[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[2]["SpecificationPairList"]:
            expan[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[3]["SpecificationPairList"]:
            front[x["Key"].replace(".", " ")] = x["Value"]
        results = dict()
        results["Model"] = model
        results["Specifications"] = specs
        results["Expansion"] = expan
        results["Front"] = front
        return results
    except:
        results = dict()
        results["Error"] = "error"
        return results


def getCPUSpecs(itemnum):
    url = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", itemnum)
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    model = dict()
    socke = dict()
    specs = dict()
    data = data["SpecificationGroupList"]
    try:
        for x in data[0]["SpecificationPairList"]:
            model[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[1]["SpecificationPairList"]:
            socke[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[2]["SpecificationPairList"]:
            specs[x["Key"].replace(".", " ")] = x["Value"]
        results = dict()
        results["Model"] = model
        results["Socket"] = socke
        results["Specifications"] = specs
        return results
    except:
        results = dict()
        results["Error"] = "error"
        return results

def getHDDSpecs(itemnum):
    url = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", itemnum)
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    model = dict()
    perfo = dict()
    physi = dict()
    data = data["SpecificationGroupList"]
    try:
        for x in data[0]["SpecificationPairList"]:
            model[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[1]["SpecificationPairList"]:
            perfo[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[2]["SpecificationPairList"]:
            physi[x["Key"].replace(".", " ")] = x["Value"]
        results = dict()
        results["Model"] = model
        results["Performance"] = perfo
        results["Physical"] = physi
        return results
    except:
        results = dict()
        results["Error"] = "error"
        return results

def getRAMSpecs(itemnum):
    url = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", itemnum)
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    model = dict()
    specs = dict()
    try:
        for x in data[0]["SpecificationPairList"]:
            model[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[1]["SpecificationPairList"]:
            specs[x["Key"].replace(".", " ")] = x["Value"].replace(".", " ")
        results = dict()
        results["Model"] = model
        results["Specification"] = specs
        return results
    except:
        results = dict()
        results["Error"] = "error"
        return results

def getMoboSpecs(itemnum):
    url = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", itemnum)
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    model = dict()
    cpu = dict()
    ram = dict()
    stora = dict()
    lan = dict()
    rearp = dict()
    physi = dict()
    data = data["SpecificationGroupList"]
    try:
        for x in data[0]["SpecificationPairList"]:
            model[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[1]["SpecificationPairList"]:
            cpu[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[3]["SpecificationPairList"]:
            ram[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[5]["SpecificationPairList"]:
            stora[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[8]["SpecificationPairList"]:
            lan[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[9]["SpecificationPairList"]:
            rearp[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[11]["SpecificationPairList"]:
            physi[x["Key"].replace(".", " ")] = x["Value"]
        results = dict()
        results["Model"] = model
        results["CPU"] = cpu
        results["Memory"] = ram
        results["Storage"] = stora
        results["LAN"] = lan
        results["Rear Panel"] = rearp
        results["Physical"] = physi
        return results
    except:
        results = dict()
        results["Error"] = "error"
        return results

def getPSUSpecs(itemnum):
    url = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", itemnum)
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    model = dict()
    specs = dict()
    data = data["SpecificationGroupList"]
    try:
        for x in data[0]["SpecificationPairList"]:
            model[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[1]["SpecificationPairList"]:
            specs[x["Key"].replace(".", " ")] = x["Value"]
        results = dict()
        results["Model"] = model
        results["Specifications"] = specs
        return results
    except:
        results = dict()
        results["Error"] = "error"
        return results

def getSSDSpecs(itemnum):
    url = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", itemnum)
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    model = dict()
    physi = dict()
    perfo = dict()
    data = data["SpecificationGroupList"]
    try:
        for x in data[0]["SpecificationPairList"]:
            model[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[1]["SpecificationPairList"]:
            physi[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[2]["SpecificationPairList"]:
            perfo[x["Key"].replace(".", " ")] = x["Value"]
        results = dict()
        results["Model"] = model
        results["Physical"] = physi
        results["Performance"] = perfo
        return results
    except:
        results = dict()
        results["Error"] = "error"
        return results

def getGPUSpecs(itemnum):
    url = "http://www.ows.newegg.com/Products.egg/{item}/Specification".replace("{item}", itemnum)
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    model = dict()
    chips = dict()
    memor = dict()
    ports = dict()
    data = data["SpecificationGroupList"]
    try:
        for x in data[0]["SpecificationPairList"]:
            model[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[2]["SpecificationPairList"]:
            chips[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[3]["SpecificationPairList"]:
            memor[x["Key"].replace(".", " ")] = x["Value"]
        for x in data[5]["SpecificationPairList"]:
            ports[x["Key"].replace(".", " ")] = x["Value"]
        results = dict()
        results["Model"] = model
        results["Chipset"] = chips
        results["Memory"] = memor
        results["Ports"] = ports
        return results
    except:
        results = dict()
        results["Error"] = "error"
        return results

def getReviews(itemnum):
    url = "http://www.ows.newegg.com/Products.egg/{item}/Reviews".replace("{item}", itemnum)
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    reviews = dict()
    reviews["Rating"] = data["Summary"]["Rating"]
    reviews["Total"] = data["Summary"]["TotalReviews"].encode("ascii", "ignore")
    return reviews

