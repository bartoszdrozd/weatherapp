from flask import Flask, render_template, request
from weather import main as get_weather

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    forecast_data = None
    date_time = None
    if request.method == 'POST':
        city = request.form['cityName']
        data, forecast_data, date_time = get_weather(city)
    return render_template('index.html', data=data, forecast_data=forecast_data, date_time=date_time)   

if __name__ == "__main__":
    app.run(debug=True)