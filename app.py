import flask
import csv
from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route("/apply",methods=["POST"])
def apply():
    in_json = flask.request.json

    if (in_json["driver_license_number"] == ""):
        current_time = datetime.now()
        print(", " + in_json["driver_license_number"] + ",       " + "DL number number not found" + ",       " + str(current_time))
        return "no DL number found -> cant initiate application process"

    current_time = datetime.now()
    print(", " + in_json["driver_license_number"] + ",       " + "application process started" + ",       " + str(current_time))

    list_of_docs=[]
    if(in_json["copies_of_id_submitted"] == "no"):
        current_time = datetime.now()
        print(", " + in_json["driver_license_number"] + ",       " + "copies of identification proof not found" + ",       " + str(current_time))
        list_of_docs.append("copies of identification proof")
    if (in_json["registration_entitle_copy_submitted"]  == "no" ):
        current_time = datetime.now()
        print(", " + in_json["driver_license_number"] + ",       " + "registration entitle copy not found" + ",       " + str(current_time))
        list_of_docs.append("registration entitle copy")
    if (in_json["is_modified"]  == "yes" ):
        if (in_json["VSCCS_submitted"] == "no"):
            current_time = datetime.now()
            print(", " + in_json["driver_license_number"] + ",       " + "VSCCS document not found" + ",       " + str(current_time))
            list_of_docs.append("VSCCS_submitted")

    if(list_of_docs != []):
        current_time = datetime.now()
        print(", " + in_json["driver_license_number"] + ",       " + "documents insufficient" + ",       " + str(current_time))
        current_time = datetime.now()
        print(", " + in_json["driver_license_number"] + ",       " + "application process completed" + ",       " + str(current_time))
        return("Please submit documents -> " + str(list_of_docs))

    with open('list_applicants.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if(row != []):
                if (row[0] == in_json["driver_license_number"]):
                    current_time = datetime.now()
                    print(", " + in_json["driver_license_number"] + ",       " + "application already exists" + ",       " + str(
                        current_time))
                    current_time = datetime.now()
                    print(", " + in_json["driver_license_number"] + ",       " + "application process completed" + ",       " + str(
                            current_time))
                    file.close()
                    return "application with same DL number found in DB: you can check the status of application"


    fields = []
    for key in in_json:
        fields.append(in_json[key])
    with open('list_applicants.csv', 'a') as file2:
        writer = csv.writer(file2)
        writer.writerow(fields)
    file2.close()
    current_time = datetime.now()
    print(", " + in_json["driver_license_number"] + ",       " + "applications db updated" + ",       " + str(current_time))

    fields = []
    fields.append(in_json["driver_license_number"])
    fields.append("Processing")
    with open('application_status.csv', 'a') as fd:
        writer = csv.writer(fd)
        writer.writerow(fields)
    fd.close()
    current_time = datetime.now()
    print(", " + in_json["driver_license_number"] + ",       " + "status db updated" + ",       " + str(current_time))

    current_time = datetime.now()
    print(", " + in_json["driver_license_number"] + ",       " + "applied successfully" + ",       " + str(current_time))
    return "applied successfully"

@app.route("/status")
def status():

    in_json = flask.request.json
    current_time = datetime.now()
    print(", " + in_json["driver_license_number"] + ",       " + "status-check initiated" + ",       " + str(current_time))

    app_status = ""
    with open('application_status.csv', 'r') as file:
        current_time = datetime.now()
        print(", " + in_json["driver_license_number"] + ",       " + "search db for status" + ",       " + str(current_time))
        reader = csv.reader(file)
        for each in reader:
            if (each != []):
                if (each[0] == in_json["driver_license_number"]):
                    app_status = each[1]
                    break
    file.close()

    if(app_status != ""):
        current_time = datetime.now()
        print(", " + in_json["driver_license_number"] + ",       " + "show application status" + ",       " + str(current_time))
        current_time = datetime.now()
        print(", " + in_json["driver_license_number"] + ",       " + "status-check completed" + ",       " + str(current_time))
        return "Status: " + app_status
    else:
        current_time = datetime.now()
        print(", " + in_json["driver_license_number"] + ",       " + "application not found" + ",       " + str(current_time))
        current_time = datetime.now()
        print(", " + in_json["driver_license_number"] + ",       " + "status-check completed" + ",       " + str(current_time))
        return "application with DL number: " + in_json["driver_license_number"] + " not found"

if __name__ == "__main__":
    app.run()
