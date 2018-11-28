# Ref: https://github.com/bhavaniravi/rasa-site-bot
from flask import Flask
from flask import render_template,jsonify,request
import requests
# from models import *
from neww import engine
import random


app = Flask(__name__)
app.secret_key = '12345'

@app.route('/')
def hello_world():
    return render_template('home.html')

get_random_response = lambda intent:random.choice(engine.intent_response_dict[intent])


@app.route('/chat',methods=["POST"])
def chat():
    try:
        user_message = request.form["text"]
        print("user_message" +user_message)
        response = requests.get("http://localhost:5000/parse",params={"q":user_message})
        response = response.json()
        entities = response.get("entities")
      
        topresponse = response["intent"]
        intent = topresponse.get("name")
        print("Intent {}, Entities {}".format(intent,entities))
        if intent == "gst-info":
            print("sujit")
            response_text = engine.gst_info(entities)# "Sorry will get answer soon" #get_event(entities["day"],entities["time"],entities["place"])
        elif intent == "gst-query":
            response_text = engine.gst_query(entities)
        else:
            response_text = get_random_response(intent)
        return jsonify({"status":"success","response":response_text})
    except Exception as e:
        print(e)
        return jsonify({"status":"success","response":"Sorry I am not trained to do that yet..."})


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8080)
