import json, urllib, urllib2

def gimages(name):
    name1 = name.replace("+","%2B")
    name2 = name1.replace(" ","%20")
    name3 = name2.replace("/","%2F")
    url = "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + name3 + "&key=AIzaSyAEH1zvTqgnRGLX8WIerdMnjZiB2Scyys0"
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    return data["responseData"]["results"][0]["unescapedUrl"]
