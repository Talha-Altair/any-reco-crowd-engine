from flask import Flask, render_template, request, jsonify
import json
app = Flask(__name__)

USERS_JSONPATH = "data.json"

@app.route('/',methods=["GET", "POST"])
def main_page():

    data = get_json()

    first_words = get_first_words(data["recommendations"])

    return render_template('index.html',json=data["recommendations"],len=len(data["recommendations"]),first_words = first_words)

def get_first_words(data):

    for i in range(len(data)):

        text = data[i]["work"]

        text = text.split()

        first_words = ''

        for i in range(7):
            first_words = first_words +' ' + str((text[i]))

        # print(first_words)

        # data[i]["first_words"] = first_words

    first_words = first_words + '...'

    return first_words

@app.route('/view/<name>',methods=["GET", "POST"])
def view_page(name):

    data = get_json()

    data = data["recommendations"]

    for i in range(len(data)):
        if data[i]["forname"]==name:
            single_data = data[i]
    
    
    return render_template('single.html',json=single_data)





@app.route('/add',methods=["GET", "POST"])
def add_recommendation():
    if request.method == "POST":
        forname = request.form.get("forname")
        byname = request.form.get("byname")
        work = request.form.get("recommendation")
        l1 = request.form.get("l1")
        l2 = request.form.get("l2")


        new_dict = {
            "forname":forname,
            "byname":byname,
            "work":work,
            "l1":l1,
            "l2":l2
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

@app.route('/admin',methods=["GET", "POST"])
def view_json():

    data = get_json()

    return jsonify(data)

@app.route('/flush',methods=["GET", "POST"])
def flush():

    return render_template('flush.html')

@app.route('/flush/confirm',methods=["GET", "POST"])
def flush_confirmed():

    data_dict = get_json()

    data_list = data_dict["recommendations"]

    data_list = []

    empty_data_dict = {
        "recommendations": data_list
    }

    with open(USERS_JSONPATH, 'w') as outfile:
        json.dump(empty_data_dict, outfile)

    return "All Recommendations has been Removed"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)