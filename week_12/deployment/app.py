"""Flask deployment app for churn prediction.

The application reads the saved sklearn model, accepts a small HTML form,
and returns a churn risk prediction based on the customer profile supplied.
"""

from __future__ import annotations

import pickle
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "deployment" / "saved_model.pkl"
TEMPLATES_DIR = PROJECT_ROOT / "deployment" / "templates"

app = Flask(__name__, template_folder=str(TEMPLATES_DIR))


with MODEL_PATH.open("rb") as model_file:
    model = pickle.load(model_file)


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the input form and produce a churn prediction when data is submitted."""
    prediction = None
    probability = None

    if request.method == "POST":
        data = {
            "Tenure": int(request.form["Tenure"]),
            "MonthlyCharges": int(request.form["MonthlyCharges"]),
            "TotalCharges": int(request.form["TotalCharges"]),
            "SeniorCitizen": int(request.form["SeniorCitizen"]),
            "Contract": request.form["Contract"],
            "PaymentMethod": request.form["PaymentMethod"],
            "PaperlessBilling": request.form["PaperlessBilling"],
        }
        row = pd.DataFrame([data])
        prediction = int(model.predict(row)[0])
        probability = float(model.predict_proba(row)[0, 1])

    return render_template(
        "index.html",
        prediction=prediction,
        probability=probability,
        churn_label="Likely to churn" if prediction == 1 else "Likely to stay",
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
