

from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import json

import stuyteachers
import html
import gmap
import gimages

app = Flask(__name__)
c = MongoClient()

fname = "data.txt"


def num(a):
    return '{:,.0f}'.format(a)



@app.route("/")
def index():

    r = ""

    if c.teachers.Collections.count() == 0:
        r += """
<div style="text-align:center;">
<h1>Attention</h1>
<h3>No teacher data has been found in the database.</h3>
</div>
<div style="margin-left:20%;margin-right:20%;width:60%;">


<div class="alert alert-success">
<div style="text-align:center;"><a href="/preload" class="btn btn-success btn-lg">Load from .txt file</a></div><br />
For your convenience, all teacher data has been preloaded using the option below and has been saved a .txt file beforehand.  To begin using <strong>StalkMyTeachers</strong> immediately you should click the above link to fill the database with all the information.<br /><br />
<em>If you are reviewing this project this is the suggested method.</em>
</div>

<div class="alert alert-warning">
<div style="text-align:center;font-size:25px;font-weight:bold;">Load from online</div><br />
<div class="alert alert-danger"><strong>Warning:</strong> This option may take an hour or more.</div><br />
Running <strong>python stuyteachers.py</strong> in command line and the program will search the internet for information about every teacher.  This loads thousands of webpages to search for information and takes quite some time.
</div>

</div>"""

    
    else:

        try:
            a = request.args.get("type")
            if a:
                r += '<div class="alert alert-success"><strong>Success:</strong> '

                if a == "1":
                    r += 'Data has been successfully loaded from .txt file into MongoDB.  Please enjoy using <strong>StalkMyTeachers</strong>!'
                elif a == "2":
                    r += 'Data has been successfully backed up into data.txt'
                r += '</div>'
        except:
            pass

#        r += '<div class="alert alert-info">Teacher value calculated as the ratio between salary and <strong>ratemyteachers.com</strong> overall rating</div>'

        r += """
<div class="alert alert-info" style="text-align:left;">
There are <strong>%d</strong> teachers and faculty members <em>(Only <strong>%d</strong> have salary information available and only <strong>%d</strong> have ratemyteachers.com information available)</em>
<br />Combined yearly salary: <strong>$%s</strong>
<br />Average salary: <strong>$%s</strong>
<br />Average ratemyteachers.com rating: <strong>%d&#37;</strong>
</div>
"""%(stuyteachers.num_teachers(),stuyteachers.num_teachers({"salary":{"$ne":-1}}),stuyteachers.num_teachers({"rmt_overall":{"$ne":-1}}),num(stuyteachers.total_salary()),num(stuyteachers.average_salary()),stuyteachers.average_rmt())

        r += '<table style="width:100%">'
        r += '<tr><td>'+html.table_overpaid(5)+'</td><td style="padding-left:20px;">'+html.table_underpaid(5)+'</td></tr>'
        r += '<tr><td>'+html.table_highestpaid(5)+'</td><td style="padding-left:20px;">'+html.table_highest("rmt_overall","Top 5 Highest Rated Teachers","Overall Rating",5)+'</td></tr>'
        r += '</table>'
    return render_template("search.html",table=r,search=html.searchCode(request.args))


@app.route("/stuylist")
def stuylist():

    if len(request.args) == 0:
        r = html.table_get("last",1,20,0)
    else:
        r = html.table_search(request.args,20,0)
        
    
    return render_template("search.html",table=r,search=html.searchCode(request.args))

#    return render_template("teacher.html",first="Mike",last="zamansky")




# TEACHER PAGE
@app.route("/teacher-<n>")
def teacher(n):
    r = ""

    d = stuyteachers.get_teacher(int(n))

    if d != None:
        r += """
<h1>%(first)s %(last)s</h1>

<div class="col-md-4">"""%(d)

        try:
            img = gimages.gImages(d['first'],d['last'])
            r += """
<table class="table table-bordered">
<tr class="active"><td style="font-weight:bold;text-align:center;">Google Images Result</td></tr>
<tr class="active"><td style="text-align:center;"><img src="%s" style="width:%spx;height:%spx;" /></td></tr>
</table>
"""%(img[2],img[0],img[1])
            
        except:

            r += """
<table class="table table-bordered">
<tr class="active"><td style="font-weight:bold;text-align:center;">Google Images Result</td></tr>
<tr class="active"><td style="text-align:center;">Error: Teacher too sexy, no results found.</td></tr>
</table>"""


        r += """
<table class="table" style="border:1px solid rgb(221, 221, 221);">
<tr class="active"><th colspan="2" style="text-align:center;">Basic Information</td></tr>
<tr class="active"><td>First Name</td><td>%(first)s</td></tr>
<tr class="active"><td>Last Name</td><td>%(last)s</td></tr>
<tr class="active"><td>Title</td><td>%(title)s</td></tr>"""%(d)

        if d["salary"] == -1:
            r += '<tr class="danger"><td colspan="2" style="text-align:center;font-weight:bold;">Salary data unavailable</td></tr>'
        else:
            d['salary'] = num(d['salary'])
            r += '<tr class="active"><td>Yearly Salary</td><td>$%(salary)s<br /><small>[As of year %(salary_year)s]</small></td></tr>'%(d)




        if d["rmt_overall"] == -1:
            r += '<tr class="danger"><td colspan="2" style="text-align:center;font-weight:bold;">Ratemyteachers.com information unavailable</td></tr>'
        else:
            r += """
<tr class="active"><td>Ratemyteachers.com</td><td>
<table>
  <tr><td style="font-weight:bold;">Overall</td><td style="font-weight:bold;">%(rmt_overall)d&#37;</td></tr>
  <tr><td>Easiness</td><td> &nbsp; %(rmt_easiness)d</td></tr>
  <tr><td>Helpfulness</td><td> &nbsp; %(rmt_helpfulness)d</td></tr>
  <tr><td>Clarity</td><td> &nbsp; %(rmt_clarity)d</td></tr>
</table>
</td></tr>
"""%(d)

        r += """
</table>

<table class="table table-bordered">
<tr class="active"><td colspan="2" style="text-align:center;font-weight:bold;">Zip Code Information</td></tr>
"""
        
        if not (len(d["address"]) > 0 and "zipinfo" in d["address"][0].keys()):
            r += '<tr class="danger"><td colspan="2" style="text-align:center;font-weight:bold">Neighborhood information unavailable</td></tr>'

        else:
            r += '<tr class="active"><td colspan="2" style="text-align:center;">The population of <strong>%d</strong> is <em>%s</em></td></tr>'%(d["zip_zip"],num(d["zip_Population"]))
            nb = [
                ["Median Income","MedianIncome","$%s"],
                ["Median Age","MedianAge","%d"],
                ["College Graduates","CollegeDegreePercent","%.1f&#37;"],
                [],
                ["Percent Married","MarriedPercent","%.1f&#37;"],
                ["Percent Divorced","DivorcedPercent","%.1f&#37;"],
                [],
                ["Percent Asian","AsianPercent","%.1f&#37;"],
                ["Percent Black","BlackPercent","%.1f&#37;"],
                ["Percent Hispanic","HispanicEthnicityPercent","%.1f&#37;"],
                ["Percent White","WhitePercent","%.1f&#37;"],
                ]

            for z in nb:
                if len(z) == 0:
                    r += '<tr class="active"><td colspan="2" style="font-size:4px;">&nbsp;</td></tr>'
                else:
                    if z[2][0] == "$":
                        r += '<tr class="active"><td>%s</td><td>%s</td></tr>'%(z[0],z[2]%(num(d["zip_"+z[1]])))
                    else:
                        r += '<tr class="active"><td>%s</td><td>%s</td></tr>'%(z[0],z[2]%(d["zip_"+z[1]]))


            

        r += """
</table>
</div>

<div class="col-md-8">
<table class="table">
<tr class="warning"><th colspan="2" style="font-weight:bold;text-align:center;">Address &amp; Phone Number Information<br />
<small><em>Click on a listing to display a Google Maps of the address</em></small></th></tr>"""

        if len(d["address"]) == 0:
            r += '<tr class="warning"><td colspan="2" style="text-align:center;">No Information Found</td></tr>'
        else:
            r += """
<tr class="warning"><td colspan="2">
<strong>Current Map:</strong><div id="curMap">%s</div><br />
<div style="text-align:center;">
<div class="btn-group">
<button type="button" onclick="mapZoomOut()" class="btn btn-default">-</button>
<button type="button" onclick="mapZoomIn()" class="btn btn-default">+</button>
</div>
<div class="btn-group">
<button type="button" onclick="mapRoadMap()" class="btn btn-default">Normal Map</button>
<button type="button" onclick="mapStreetView()" class="btn btn-default">Street View</button>
</div>

<br /><br />
<img src="%s" id="mapImg" />
</div>
</td></tr>"""%(d["address"][0]["address"],gmap.gmap(d["address"][0]["address"]))

            aw = "success"
            for x in d["address"]:
                r += '<tr class="%s mapListing"><td colspan="2"><a href="javascript:void(0)" style="font-weight:bold;">%s</a><br />%s</td></tr>'%(aw,x["address"],x["phoneNum"])
                aw = "warning"


        r += """

</table>
</div>
"""%(d)


    return render_template("search.html",table=r,search=html.searchCode({}))



# departments
@app.route("/department")
def department():
    r = ""

    r += """<table class="table table-striped table-bordered" id="depTable">
<tr class="active">
<th colspan="4" style="font-style:italic;text-align:center;">Click a column header below to sort</th>
</tr>
<tr class="active" class="col_heads active">
<th><a href="javascript:void(0)" onclick="sortDep(0,1)">Department</a></th>
<th><a href="javascript:void(0)" onclick="sortDep(1,-1)"># Teachers</a></th>
<th><a href="javascript:void(0)" onclick="sortDep(2,-1)">Average Salary</a></th>
<th><a href="javascript:void(0)" onclick="sortDep(3,-1)">Average Rating</a></th>
</tr>"""


    js = []

    for x in sorted(stuyteachers.get_departments()):
        k = stuyteachers.get_teachers_in_department(x)

        salary = []
        rating = []
        
        for y in k:
            if y["salary"] != -1:
                salary.append(y["salary"])
            if y["rmt_overall"] != -1:
                rating.append(y["rmt_overall"])
                
        sal = sum(salary)/len(salary)
        rat = sum(rating)/len(rating)


        r += '<tr><td><a href="stuylist?title=%s">%s</a></td><td><span>%d</span></td><td>$<span>%s</span></td><td><span>%d</span>&#37;</td></tr>'%(x.replace(" ","+"),x,len(k),num(sal),rat)
        js.append('["%s",%d,"%s",%d]'%(x,len(k),num(sal),rat))

    r += '</table>'

    r += '<script type="text/javascript">tab = ['+",".join(js)+'];</script>'

    return render_template("search.html",table=r,search=html.searchCode({}))





@app.route("/js")
def js():
    
    param = "last"
    sort = 1
    limit = 20
    offset = 0

    try:
        param = request.args.get("param")
        sort = request.args.get("sort")
        offset = request.args.get("offset")
    except:
        pass

    nam = None
    if "name" in request.args:
        nam = request.args.get("name")


    try:
        return str(html.table_get(param,sort,limit,int(offset)))
    except:
        return '{error:true}'


@app.route("/teacherjs-<n>")
def teacherjs(n):
    r = ""

    first = n.split("+")[0]

    a = c.teachers.Collections.find_one({"first":first,"last":n.replace(first+"+","")})

    path = ""
    r += """ 
<table class="table table-bordered">
<tr class="active"><td colspan="2"><a href="teacher-%(id)d"><h1>%(first)s %(last)s</h1></a></td></tr>"""%(a)
    r += '<tr class="active"><td colspan="2"><strong>%s</strong><br />%s'%(a["address"][0]["address"],a["address"][0]["phoneNum"])
    r += """
<tr class="active"><td>Title</td><td>%(title)s</td></tr>"""%(a)

    if a["salary"] == -1:
        r += '<tr class="danger"><td colspan="2" style="text-align:center;font-weight:bold;">Salary data unavailable</td></tr>'
    else:
        a['salary'] = num(a["salary"])
        r += '<tr class="active"><td>Yearly Salary</td><td>$%(salary)s<br /><small>[As of year %(salary_year)s]</small></td></tr>'%(a)

    if a["rmt_overall"] == -1:
        r += '<tr class="danger"><td colspan="2" style="text-align:center;font-weight:bold;">Ratemyteachers.com information unavailable</td></tr>'
    else:
        r += """
<tr class="active"><td>Ratemyteachers.com</td><td>
<table>
  <tr><td style="font-weight:bold;">Overall</td><td style="font-weight:bold;">%(rmt_overall)d&#37;</td></tr>
  <tr><td>Easiness</td><td> &nbsp; %(rmt_easiness)d</td></tr>
  <tr><td>Helpfulness</td><td> &nbsp; %(rmt_helpfulness)d</td></tr>
  <tr><td>Clarity</td><td> &nbsp; %(rmt_clarity)d</td></tr>
</table>
</td></tr>"""%(a)

    r += '</table>'


    if len(a["address"]) > 0 and len(a["address"][0]["directions"]["routes"]):
        b = a["address"][0]["directions"]["routes"][0]["legs"][0]
        path = str(a["address"][0]["directions"]["routes"][0]["legs"][0]["steps"])
        r += """
<div class="btn-group">
<button class="btn btn-primary" onclick="viewDirections(0)">MTA Directions</button>
<button class="btn btn-info" onclick="viewDirections(1)">CitiBike Directions</button>
</div><br />
<div class="panel panel-primary directions" style="display:none"><div class="panel-heading">MTA Information</div><div class="panel-body">
<strong>Commute Distance to Stuyvesant:</strong> %s<br />
<strong>Commute Time to Stuyvesant:</strong> %s<br />
<div id="publicTransitDetails">&nbsp;</div>
</div></div>"""%(b["distance"]["text"],b["duration"]["text"])

        if "citibike" in a["address"][0].keys():
            cc = a["address"][0]["citibike"]
            r += """
<div class="panel panel-info directions" style="display:none"><div class="panel-heading">CitiBike Information</div><div class="panel-body">
<strong>Nearest CitiBike Station:</strong> %s<br />
<strong>Walking Distance to CitiBike Station:</strong> %s<br />
<strong>Walking Time to CitiBike Station:</strong> %s<br />
<strong>CitiBike Distance to Stuyvesant:</strong> %s<br />
<strong>CitiBike Time to Stuyvesant:</strong> %s<br />
</div></div>"""%(cc["bike_station"],cc["walk_distance"],cc["walk_time"],cc["bike_distance"],cc["bike_time"])

            r += """<script type="text/javascript">
cb = ["%s","%s"];
</script>"""%(cc["bike_polyline"]["points"].replace("\\","\\\\"),cc["walk_polyline"]["points"].replace("\\","\\\\"))

        else:
            r += """
<div class="panel panel-info directions" style="display:none"><div class="panel-heading">CitiBike Information</div><div class="panel-body">
Only available to teachers who live in Manhattan and Brooklyn</div></div>"""

        r += """
<script type="text/javascript">
cp = %s;
</script>
"""%(path.replace("u'","'"))
#        path = a["address"][0]["directions"]["routes"][0]["overview_polyline"]["points"]


    return r
#    return '%s %s'%(path,r)


@app.route("/all")
def showAll():
    r = """
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <link rel="shortcut icon" href="../static/stalkmyteachers.jpg">
    <title>StalkMyTeachers - Map</title>
    <style>
      html, body, #map-canvas {
        height: 100%;
        margin: 0px;
        padding: 0px
      }
    </style>
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&libraries=geometry"></script>
    <script src="https://code.jquery.com/jquery.js"></script>
    <link href="../static/bootstrap/css/bootstrap.css" rel="stylesheet">
    <script>

addr = ["""

    k = []

    for x in c.teachers.Collections.find():
        if len(x["address"]) > 0 and "lat" in x["address"][0]:
            k.append('["'+x["first"]+' '+x["last"]+'",'+str(x["address"][0]["lat"])+','+str(x["address"][0]["long"])+']')

    r += ",".join(k)

    r+= """];
    </script>
    <script type="text/javascript" src="static/maps.js"></script>
  </head>
  <body>
      <div id="map-canvas"></div>
      <div style="position:fixed;background:white;top:0;right:0;width:400px;z-index:999;height:100%;border-left:4px solid black;padding:0;overflow:auto;">
<div style="text-align:center;border-bottom:2px solid black;padding:5px;"><a href="/">Back to Home Page</a></div>
<div id="sidebar" style="padding:5px;">
<h1>
Hover over a pin to see who lives there.
<br /><br />
Click a pin to load teacher information.
</h1>
</div>
</div>
  </body>
</html>
"""
    return r


@app.route("/preload")
def preload():
    f = open(fname,"r")
    a = json.loads(f.read())#.replace("{u'",'{"').replace("'",'"'))

    for x in a:
        del x["_id"]

#    a = eval(f.read().replace("ObjectId(","").replace("'),","',"))

#    return str(a)


    if c.teachers.Collections.count() == 0:
        for x in a:
            c.teachers.Collections.insert(x)

    return redirect("/?type=1")#"Preload successful<br /><br /><a href='/'>Go Home</a>"

@app.route("/backup")
def backup():

    if c.teachers.Collections.count() > 0:
        f = open(fname,"w")

        a = []
        for x in c.teachers.Collections.find():
            x["_id"] = None
            a.append(x)

        f.write(json.dumps(a))

        return redirect("/?type=2")#"Backup successful<br /><br /><a href='/'>Go Home</a>"

@app.route("/loadall")
def loadall():
    stuyteachers.teachersToDatabase()

    return "Load successful<br /><br /><a href='/'>Go Home</a>"


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0",port=6008)
