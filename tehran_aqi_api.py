# tehran_aqi_api.py
# ------------------------
# Simple Tehran AQI API (scraping from airnow.tehran.ir)

from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_tehran_aqi():
    try:
        url = "https://airnow.tehran.ir/"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # پیدا کردن شاخص در صفحه
        aqi_box = soup.find("span", {"id": "ctl00_ContentPlaceHolder1_lblAQIIndex"})
        status_box = soup.find("span", {"id": "ctl00_ContentPlaceHolder1_lblAQIStatus"})

        if not aqi_box:
            return {"error": "AQI not found"}

        return {
            "aqi": aqi_box.text.strip(),
            "status": status_box.text.strip() if status_box else "Unknown"
        }

    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    return jsonify({"message": "Tehran AQI API Active"})

@app.route("/aqi")
def aqi_endpoint():
    data = scrape_tehran_aqi()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
