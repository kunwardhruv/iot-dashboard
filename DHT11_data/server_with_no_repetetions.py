from flask import Flask, jsonify
import serial
import joblib
import threading
import time
from datetime import datetime  # For timestamp

app = Flask(__name__)
model = joblib.load("DHT11_model.pkl")

# Global variables to store latest data
latest_temp = None
latest_hum = None
latest_status = None
latest_time = None

# Track previous temperature
previous_temp = None

# ✅ CHANGE: Add a flag to track data update
data_updated = False  # ✅ CHANGE

# Setup serial connection
ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)  # wait for Arduino to initialize

def read_from_arduino():
    global latest_temp, latest_hum, latest_status, latest_time
    global previous_temp, data_updated  # ✅ CHANGE

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(',')
                if len(parts) == 2:
                    temp = float(parts[0])   # change from float to int
                    hum = float(parts[1])

                    # Always predict using both temp and hum
                    prediction = model.predict([[temp, hum]])[0]
                    status = "NORMAL" if prediction == 0 else "FAILURE"

                    # ✅ CHANGE: Update only if temperature changes
                    if temp != previous_temp:
                        latest_temp = temp
                        latest_hum = hum
                        latest_status = status
                        latest_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        previous_temp = temp
                        data_updated = True  # ✅ CHANGE

                        print(f"[{latest_time}] Temp: {temp}, Humidity: {hum} => Prediction: {status}")

            time.sleep(1)

        except Exception as e:
            print("Error reading Arduino:", e)

# Background thread to read serial
threading.Thread(target=read_from_arduino, daemon=True).start()

@app.route('/get_status', methods=['GET'])
def get_status():
    global data_updated  # ✅ CHANGE

    if latest_temp is None or latest_hum is None or latest_status is None:
        return jsonify({'error': 'No data yet from sensor'}), 503

    # ✅ CHANGE: Return only if new data is available
    if not data_updated:
        return '', 204  # No new data

    data_updated = False  # ✅ CHANGE: Reset the flag after sending

    return jsonify({
        'temperature': latest_temp,
        'humidity': latest_hum,
        'status': latest_status,
        'timestamp': latest_time
    })

if __name__ == '__main__':
    print("Server started, reading Arduino continuously...")
    app.run(host='0.0.0.0', port=5000)
