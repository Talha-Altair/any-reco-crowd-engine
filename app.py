from flask import Flask, render_template, request, jsonify
import json
app = Flask(__name__)

USERS_JSONPATH = "data.json"

@app.route('/') #Defining Root Node
def main_page():

    data = get_json()

    return render_template('view.html',json=data["recommendations"],len=len(data["recommendations"]))


@app.route('/add',methods=["GET", "POST"]) #Defining Root Node
def add_recommendation():
    if request.method == "POST":
        forname = request.form.get("forname")
        byname = request.form.get("byname")
        work = request.form.get("recommendation")

        new_dict = {
            "forname":forname,
            "byname":byname,
            "work":work
        }

        data = get_json()

        data["recommendations"].append(new_dict)

        store_data(data)

    return render_template('admin.html')

def get_json():

    json_file = open(USERS_JSONPATH)
    json_data = json.load(json_file)

    return json_data

def store_data(json_data):

    with open(USERS_JSONPATH, 'w') as outfile:
        json.dump(json_data, outfile)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)