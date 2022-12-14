import joblib
from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__,static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300

# No cacheing at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

CORS(app)

@app.route('/',methods=['GET'])
def sendHomePage():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def PredictPossibility():
    GREScore = float(request.form['GREScore'])
    TOEFLScore = float(request.form['TOEFLScore'])
    UnivRating = float(request.form['UnivRating'])
    SOP = float(request.form['SOP'])
    LOR = float(request.form['LOR'])
    CGPA = float(request.form['CGPA'])
    Research = 0
    if('Research' in request.form):
        Research = 1
    X = [[GREScore , TOEFLScore , UnivRating , SOP , LOR , CGPA , Research ]]
    model = joblib.load('model/Admission_Predictor.pkl')
    scale = joblib.load('scalers/Data_Scaler.z')
    target_scale = joblib.load('scalers/Target_Scaler.z')
    print(X)
    X = scale.transform(X)
    print(X)
    probability = (target_scale.inverse_transform(model.predict(X))[0][0].round(2)) *100
    print(probability)
    prob_comment = ""
    color_scheme = ""
    if(probability > 100):
        probability = 100
    elif(probability < 0):
        probability = 0
    if(probability < 50):
        prob_comment = "The Chances of Getting an Admission is less likely"
        color_scheme = 'darkorange'
    elif(probability < 70):
        prob_comment = "There is a slight Chance of Possibility."
        color_scheme = 'yellow'
    else:
        prob_comment = "There is High Chances of Possibility"
        color_scheme = 'lawngreen'
    return render_template('predict.html',predict=probability,comment=prob_comment,color_scheme=color_scheme)

if __name__ == '__main__':
    app.run(debug = True)