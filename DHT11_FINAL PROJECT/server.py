from flask import Flask, jsonify, render_template
import serial
import serial.tools.list_ports
import joblib
import threading
import time
from datetime import datetime
import subprocess
import pandas as pd
import re

app = Flask(__name__)
model = joblib.load("DHT11_model.pkl")

latest_temp = None
latest_hum = None
latest_status = None
latest_time = None

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "Arduino" in port.description or "USB Serial" in port.description:
            return port.device
    return None

arduino_port = find_arduino_port()
if arduino_port:
    try:
        ser = serial.Serial(arduino_port, 9600, timeout=1)
        time.sleep(2)
        print(f"\nArduino connected on {arduino_port}\n")
    except Exception as e:
        print(f"Error opening port {arduino_port}: {e}")
        ser = None
else:
    print("Arduino not found.")
    ser = None

def read_from_arduino():
    global latest_temp, latest_hum, latest_status, latest_time
    if not ser:
        print("No serial connection.")
        return
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(',')
                if len(parts) == 2:
                    temp = float(parts[0])
                    hum = float(parts[1])
                    input_df = pd.DataFrame([[temp, hum]], columns=["Temperature (°C)", "Humidity (%)"])
                    prediction = model.predict(input_df)[0]
                    status = "NORMAL" if prediction == 0 else "FAILURE"

                    latest_temp = temp
                    latest_hum = hum
                    latest_status = status
                    latest_time = datetime.now().strftime("%H:%M:%S")

                    print(f"Temp: {temp} C, Humidity: {hum} %, Prediction: {status}")
            time.sleep(1)
        except Exception as e:
            print("Error reading Arduino:", e)

if ser:
    threading.Thread(target=read_from_arduino, daemon=True).start()

@app.route('/get_status', methods=['GET'])
def get_status():
    if latest_temp is None or latest_hum is None or latest_status is None:
        return jsonify({'error': 'No data yet from sensor'}), 503

    return jsonify({
        'temperature': latest_temp,
        'humidity': latest_hum,
        'status': latest_status,
        'timestamp': latest_time
    })

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

def start_cloudflare_tunnel():
    try:
        tunnel = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", "http://localhost:5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        output = ""
        for line in tunnel.stdout:
            print(line.strip())  # Show logs
            output += line
            # Match the actual URL using regex
            match = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", output)
            if match:
                url = match.group(0)
                print("\n Public Dashboard:", url + "/")
                print(" Sensor API:", url + "/get_status\n")
                break
    except Exception as e:
        print(" Error starting Cloudflare Tunnel:", e)


if __name__ == '__main__':
    print("Starting Server & Tunnel...\n")
    threading.Thread(target=start_cloudflare_tunnel, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
