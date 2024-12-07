from flask import Flask, render_template, jsonify
import readData as rd
import json

app = Flask(__name__)

# Trend data storage
trend_data = []

@app.route('/')
def display_data():
    return render_template('index.html')

@app.route('/api/total-balance', methods=['GET'])
def get_total_balance():
    try:
        # Fetch data from your custom function
        api_data = rd.myBalance()
        api_data_json = json.loads(api_data.text)
        if "balances" not in api_data_json:
            raise KeyError("Key 'balances' not found in the API response")
        
        # Calculate total AUD balance
        total_audbalance = round(sum(
            item[next(iter(item))]["audbalance"]
            for item in api_data_json["balances"]
        ), 0)
    except Exception as e:
        print(f"Error fetching total balance: {e}")
        total_audbalance = 0  # Fallback value

    return jsonify({"total_audbalance": total_audbalance})

@app.route('/trend')
def trend_page():
    return render_template('trend.html')

@app.route('/api/trend-data', methods=['GET'])
def get_trend_data():
    global trend_data
    try:
        # Fetch data from your custom function
        api_data = rd.myBalance()
        api_data_json = json.loads(api_data.text)
        if "balances" not in api_data_json:
            raise KeyError("Key 'balances' not found in the API response")
        
        # Calculate total AUD balance for the trend
        new_value = round(sum(
            item[next(iter(item))]["audbalance"]
            for item in api_data_json["balances"]
        ), 0)
    except Exception as e:
        print(f"Error updating trend data: {e}")
        new_value = 0  # Fallback value

    # Update the trend data
    trend_data.append(new_value)
    if len(trend_data) > 20:
        trend_data.pop(0)  # Keep only the last 20 values

    return jsonify(trend_data)

if __name__ == '__main__':
    app.run(debug=True)
