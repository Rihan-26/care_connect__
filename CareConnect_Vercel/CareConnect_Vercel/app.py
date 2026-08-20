from flask import Flask, render_template, request, jsonify

from orchestrator import orchestrator
from agents.doctor_locator import doctor_locator_agent

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyzing")
def analyzing():
    return render_template("analyzing.html")


@app.route("/results")
def results():
    return render_template("result.html")


# ============================================
# AI Symptom Analysis
# ============================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        symptoms = data["symptoms"]
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])

        result = orchestrator.process(
            symptoms,
            latitude,
            longitude
        )

        return jsonify(result)

    except Exception as e:

        import traceback

        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500
# ============================================
# Nearby Hospitals (Real OpenStreetMap Data)
# ============================================

@app.route("/nearby-hospitals", methods=["POST"])
def nearby_hospitals():

    data = request.get_json()

    latitude = float(data["latitude"])
    longitude = float(data["longitude"])

    hospitals = doctor_locator_agent.search(
        latitude,
        longitude
    )

    return jsonify(hospitals)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)