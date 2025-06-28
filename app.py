from flask import Flask, render_template, request
import numpy as np
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = None
    if request.method == "POST":
        try:
            dBm = float(request.form["dBm"])  #dBm
            result = np.round(10**(dBm/10), 4)           #mW
        except ValueError:
            result = "Invalid input"
    return render_template("calculator.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)