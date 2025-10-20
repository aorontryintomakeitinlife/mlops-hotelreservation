import joblib ##loading model
import numpy as np ## to give input to the model only thne model can give prediction same as in jupyter
from config.paths_config import MODEL_OUTPUT_PATH ##FROM HERE WE LOAD MODEL
from flask import Flask,request,render_template

app=Flask(__name__)

loaded_model = joblib.load(MODEL_OUTPUT_PATH)

###SETTING A ROUTE
@app.route("/", methods=["GET" , "POST"])###"/ "- home page. ##3we get data from html code to flask , and we need to get data from html what was inpiutted and we need to post back the predictions into index html 
def index():
    if request.method=="POST":
        print(request.form)
        ###for this we need to fisrt get the data
        lead_time=int(request.form["lead_time"]) ##we need to convert it into integer , incase if its in string format , we need to ensure its in integer
        no_of_special_request=int(request.form["no_of_special_requests"])
        avg_price_per_room=float(request.form["avg_price_per_room"])
        arrival_month=int(request.form["arrival_month"])
        arrival_date=int(request.form["arrival_date"])
        market_segment_type=int(request.form["market_segment_type"])
        no_week_nights=int(request.form["no_of_week_nights"])
        no_of_weekend_nights=int(request.form["no_of_weekend_nights"]) ###make sure id same as indexhtml
        type_of_meal_plan=int(request.form["type_of_meal_plan"])
        room_type_reserved=int(request.form["room_type_reserved"])
        
        ###now we need to convert all this data to numpy array

        features=np.array([[lead_time,no_of_special_request,avg_price_per_room,arrival_month,arrival_date,market_segment_type,no_week_nights,no_of_weekend_nights,type_of_meal_plan,room_type_reserved]])
        prediction=loaded_model.predict(features)
        ###help show our resilt in html file
        return render_template("index.html", prediction=prediction[0]) ##we need only 1st index ,refer jupyter notebook, we are extracting the value here 
    
    
    ###this is else case . we get no input , it shoukd be running fine thats why none is given
    return render_template("index.html" , prediction=None) 

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)

        








