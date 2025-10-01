# 📌 IoT-based Temperature & Humidity Monitoring with Dashboard
## 🚀 Project Overview

This project is an IoT system that collects real-time temperature and humidity data using a DHT11 sensor and Arduino.
The data is sent to a Flask-based server, stored in CSV format, analyzed with a trained ML model, and visualized on a dark-themed dashboard.

The system also predicts failure conditions when:

🌡️ Temperature > 35°C

💧 Humidity > 60%
---
# 🗂️ Folder Structure
```
IOT + DASHBOARD/
│
├── DHT11_data/                 # Data collection & model training
│   ├── basic_server.py         # Simple Flask server
│   ├── DHT11_model.pkl         # Trained ML model
│   ├── model.ipynb             # Jupyter Notebook (training code)
│   ├── read_to_predict.py      # Read live data & predict failures
│   ├── save_data.py            # Save data into CSV
│   ├── server_with_no_repetetions.py # Improved Flask server
│   └── updated_dht11_with_failures.csv # Dataset with failure labels
│
├── DHT11_FINAL PROJECT/        # Final working project
│   ├── templates/
│   │   └── dashboard.html      # Dark themed dashboard UI
│   ├── Arduino_Code.ino        # Arduino code for DHT11
│   ├── cloudflared.exe         # Tunnel for public access
│   ├── DHT11_model.pkl         # Final trained ML model
│   ├── requirements.txt        # Python dependencies
│   └── server.py               # Flask server with dashboard
│
└── README.md                   # Project documentation

```
---

# ⚙️ Installation

```
1️⃣ Clone the Repository
git clone https://github.com/kunwardhruv/iot-dashboard.git
cd iot-dashboard/DHT11_FINAL PROJECT

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Connect Arduino

Upload Arduino_Code.ino to Arduino board.

Ensure DHT11 sensor is connected properly.

4️⃣ Run Flask Server
python server.py

5️⃣ Access Dashboard
Open your web browser and go to http://localhost:5000

```
---

# 📊 Features

```

✔️ Real-time Temperature & Humidity monitoring
✔️ Data logging in CSV
✔️ ML model to predict system failures
✔️ Interactive dark-themed dashboard
✔️ Works locally & remotely (via Cloudflare Tunnel)

```

# 🛠️ Tech Stack

Hardware: Arduino + DHT11 Sensor

Backend: Flask (Python)

Frontend: HTML + Chart.js

ML Model: Scikit-learn (trained model saved as .pkl)
