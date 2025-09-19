# read arduino data and predict using trained model


import serial
import joblib
import pandas as pd

# Load trained model
model = joblib.load('DHT11_model.pkl')

# Connect to Arduino serial
ser = serial.Serial('COM7', 9600, timeout=1)  # Change COM port if needed
print(" Waiting for data from Arduino...")

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            temp_hum = line.split(',')
            if len(temp_hum) == 2:
                temperature = float(temp_hum[0])
                humidity = float(temp_hum[1])

                # Use DataFrame to match training format
                input_data = pd.DataFrame([[temperature, humidity]], columns=["Temperature (°C)", "Humidity (%)"])

                # Predict
                prediction = model.predict(input_data)[0]
                status = "FAILURE DETECTED" if prediction == 1 else "NORMAL"

                # Use ASCII-safe output
                print(f"Temp: {temperature}, Humidity: {humidity} => Prediction: {status}")
    except Exception as e:
        print("Error:", e)
