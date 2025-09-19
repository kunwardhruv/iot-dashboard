import serial
import csv
from datetime import datetime

# ========== SETTINGS ==========
SERIAL_PORT = 'COM7'     # Change this to your Arduino's COM port
BAUD_RATE = 9600
OUTPUT_FILE = 'dht11_log.csv'
# ==============================

# Open serial port
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
print("Connected to Arduino. Logging started...")

# Open CSV file for writing
with open(OUTPUT_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['Index', 'Timestamp', 'Temperature (°C)', 'Humidity (%)'])

    index = 1  # Start index from 1

    while True:
        try:
            # Read a line from Serial and decode it
            line = ser.readline().decode('utf-8').strip()

            # Expecting "temperature,humidity"
            if "," in line:
                temp, hum = line.split(',')
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Write row to CSV
                writer.writerow([index, timestamp, temp, hum])
                file.flush()  # Ensure it writes immediately

                # Print to console
                print(f"{index}. {timestamp} | Temp: {temp}°C | Humidity: {hum}%")

                index += 1  # Increment index
        except KeyboardInterrupt:
            print("Logging stopped by user.")
            break
        except Exception as e:
            print("Error:", e)
