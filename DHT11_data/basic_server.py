from flask import Flask, jsonify
import serial
import joblib
import threading
import time

app = Flask(__name__)
model = joblib.load("DHT11_model.pkl")

# Global variables to store latest data
latest_temp = None
latest_hum = None
latest_status = None

# Setup serial connection
ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)  # wait for Arduino

def read_from_arduino():
    global latest_temp, latest_hum, latest_status
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(',')
                if len(parts) == 2:
                    temp = float(parts[0])
                    hum = float(parts[1])
                    prediction = model.predict([[temp, hum]])[0]
                    status = "NORMAL" if prediction == 0 else "FAILURE"

                    # Update latest values
                    latest_temp = temp
                    latest_hum = hum
                    latest_status = status

                    print(f"Temp: {temp}, Humidity: {hum} => Prediction: {status}")

            time.sleep(1)  # small delay to avoid CPU hogging
        except Exception as e:
            print("Error reading Arduino:", e)

# Start the background thread to read data continuously
threading.Thread(target=read_from_arduino, daemon=True).start()

@app.route('/get_status', methods=['GET'])
def get_status():
    if latest_temp is None or latest_hum is None or latest_status is None:
        return jsonify({'error': 'No data yet from sensor'}), 503
    
    return jsonify({
        'temperature': latest_temp,
        'humidity': latest_hum,
        'status': latest_status
    })

if __name__ == '__main__':
    print("Server started, reading Arduino continuously...")
    app.run(host='0.0.0.0', port=5000)
