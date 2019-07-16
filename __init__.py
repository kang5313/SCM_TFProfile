from flask import Flask, redirect,request,send_file,jsonify,render_template
from flask_cors import CORS
from datetime import date,datetime
import xml.etree.ElementTree as xml
from lxml import etree
import time as mod_time
import json
import os

profileCollectionVersion = "1.0"
profileVersion = "1.0"
description = "This is Profile Collection v1.0"
app = Flask(__name__,static_folder="build/static",template_folder="build")
CORS(app)

@app.route('/',methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/',methods=['POST'])
def JSONtoXML():
    json_data = json.loads(request.data)
    createddate = str(date.today())
    now = datetime.now()
    timestamp = str((mod_time.mktime(now.timetuple())+now.microsecond/1000000.0))
    root = etree.Element("profilecollection")
    root.set('version','1.0')

    L1Element = etree.Element("profile")
    L1Element.set('version',profileVersion)
    L1Element.set('name',json_data[2])
    L1Element.set('createddate',createddate)
    L1Element.set('selectedTechFlowVersion',json_data[1])
    root.append(L1Element)

    L2Element_1 = etree.SubElement(L1Element, "description")
    L2Element_1.text = description
    L2Element_2 = etree.SubElement(L1Element,"variablecollection")

    for profile in json_data[0]:
        L3Element = etree.SubElement(L2Element_2,"variable")
        L3Element.set('name',profile['variableName'])
        L3Element.set('category',profile['category'])
        L4Element = etree.SubElement(L3Element,'value')
        if('selectedValue' in profile):
            if(isinstance(profile['selectedValue'],list)):
                multipleSelectedValue = ",".join(profile['selectedValue'])
                L4Element.text=multipleSelectedValue
            else:
                L4Element.text = profile['selectedValue']
        else:
            L4Element.text = profile['value']
    
    tree = etree.ElementTree(root)
    if(not os.path.exists("./upload")):
        os.makedirs("./upload")
    filename = "./upload/SampleProfile_"+timestamp+".tprof"
    tree.write(filename,pretty_print=True)
    return filename

@app.route('/xml/<path:filename>')
def download(filename):
    return send_file(filename,as_attachment=True)

if __name__ == "__main__":
    app.run(port=8000,debug=True)