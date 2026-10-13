
import os
import json
import sqlite3
from pathlib import Path

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session
)
from werkzeug.utils import secure_filename
import numpy as np

BASE = Path(__file__).resolve().parent
DB = BASE / "agrisaahayak.db"
UPLOADS = BASE / "uploads"
UPLOADS.mkdir(exist_ok=True)

MODEL_PATH = BASE / "model" / "agrisaahayak_model.keras"
CLASS_PATH = BASE / "model" / "class_names.json"

app = Flask(__name__)
app.secret_key = "change-this-secret-in-production"

ALLOWED = {"png", "jpg", "jpeg", "webp"}

LANGUAGES = {
    "en": "English",
    "hi": "हिंदी",
    "mr": "मराठी"
}

# All text used by the home and prediction pages
TRANSLATIONS = {
    "en": {
        "home": "Home",
        "predict": "Crop Disease Detection",
        "workers": "Find Farm Workers",
        "register": "Register Worker",
        "dashboard": "Dashboard",
        "welcome": "Welcome to AgriSahayak AI",
        "tagline": "Smart farming assistance for every farmer",
        "hero_text": "Identify possible crop diseases using a leaf image.",
        "get_started": "Detect Crop Disease",
        "features": "Our Services",
        "feature1": "AI Disease Detection",
        "feature1_text": "Upload a crop leaf photo to check for a possible disease.",
        "feature2": "Find Farm Workers",
        "feature2_text": "Find workers for your agricultural needs.",
        "feature3": "Easy to Use",
        "feature3_text": "Simple tools to help farmers make informed decisions.",
        "language": "Choose Language",
        "footer": "Helping farmers grow better",
        "upload_title": "Crop Disease Detection",
        "upload_text": "Upload a clear photo of a crop leaf.",
        "choose_image": "Choose Leaf Image",
        "predict_button": "Detect Disease",
        "result": "Prediction Result",
        "disease": "Possible Disease",
        "confidence": "Model Confidence",
        "symptoms": "Common Symptoms",
        "prevention": "Prevention Tips",
        "try_again": "Try Another Image",
        "no_result": "Upload a leaf image to get a prediction.",
        "choose_error": "Please choose an image first.",
        "invalid_error": "Use a JPG, JPEG, PNG or WEBP image.",
        "prediction_error": "Sorry, the image could not be processed.",
        "healthy": "Healthy Leaf",
        "early": "Tomato Early Blight",
        "late": "Tomato Late Blight",
        "leaf_mold": "Tomato Leaf Mold",
        "unknown": "Unknown Disease",
        "healthy_symptoms": "No disease was identified by the model. Continue checking the plant regularly.",
        "early_symptoms": "Dark spots may appear on older leaves, sometimes with ring-like patterns and yellowing.",
        "late_symptoms": "Water-soaked, dark or irregular spots may appear on leaves and spread quickly in wet conditions.",
        "mold_symptoms": "Yellow patches may appear on the upper leaf surface, with olive-green or brown growth underneath.",
        "healthy_prevention": "Keep checking leaves regularly, water near the soil, and maintain good airflow.",
        "early_prevention": "Remove badly affected leaves, avoid wetting foliage, and follow local agricultural advice for disease management.",
        "late_prevention": "Remove affected plant material safely, avoid overhead watering, and seek local agricultural advice promptly.",
        "mold_prevention": "Improve airflow, avoid wet leaves, remove badly affected material, and seek local agricultural advice.",
        "unknown_symptoms": "The model could not match this result to a known disease description.",
        "unknown_prevention": "Take a clear photo and ask a local agricultural officer for confirmation."
    },

    "hi": {
        "home": "होम",
        "predict": "फसल के रोग की पहचान",
        "workers": "खेत मजदूर खोजें",
        "register": "मजदूर का पंजीकरण",
        "dashboard": "डैशबोर्ड",
        "welcome": "AgriSahayak AI में आपका स्वागत है",
        "tagline": "हर किसान के लिए स्मार्ट खेती सहायता",
        "hero_text": "पत्ते की फोटो से संभावित फसल रोग की पहचान करें।",
        "get_started": "फसल का रोग पहचानें",
        "features": "हमारी सेवाएँ",
        "feature1": "AI से रोग की पहचान",
        "feature1_text": "संभावित रोग जानने के लिए पत्ते की फोटो अपलोड करें।",
        "feature2": "खेत मजदूर खोजें",
        "feature2_text": "खेती के काम के लिए मजदूर खोजें।",
        "feature3": "आसान उपयोग",
        "feature3_text": "किसानों के लिए सरल और उपयोगी सुविधाएँ।",
        "language": "भाषा चुनें",
        "footer": "किसानों की बेहतर खेती में सहायता",
        "upload_title": "फसल के रोग की पहचान",
        "upload_text": "फसल के पत्ते की साफ फोटो अपलोड करें।",
        "choose_image": "पत्ते की फोटो चुनें",
        "predict_button": "रोग पहचानें",
        "result": "पहचान का परिणाम",
        "disease": "संभावित रोग",
        "confidence": "मॉडल का विश्वास स्तर",
        "symptoms": "सामान्य लक्षण",
        "prevention": "बचाव के उपाय",
        "try_again": "दूसरी फोटो आज़माएँ",
        "no_result": "रोग की पहचान के लिए पत्ते की फोटो अपलोड करें।",
        "choose_error": "कृपया पहले फोटो चुनें।",
        "invalid_error": "JPG, JPEG, PNG या WEBP फोटो का उपयोग करें।",
        "prediction_error": "माफ़ कीजिए, फोटो की जाँच नहीं हो सकी।",
        "healthy": "स्वस्थ पत्ता",
        "early": "टमाटर में अर्ली ब्लाइट रोग",
        "late": "टमाटर में लेट ब्लाइट रोग",
        "leaf_mold": "टमाटर में लीफ मोल्ड रोग",
        "unknown": "अज्ञात रोग",
        "healthy_symptoms": "मॉडल ने कोई रोग नहीं पहचाना। पौधे की नियमित जाँच करते रहें।",
        "early_symptoms": "पुरानी पत्तियों पर गहरे धब्बे, छल्ले जैसे निशान और पीलापन दिखाई दे सकता है।",
        "late_symptoms": "पत्तियों पर गीले जैसे गहरे या अनियमित धब्बे दिख सकते हैं और नमी में तेजी से फैल सकते हैं।",
        "mold_symptoms": "पत्तियों के ऊपर पीले धब्बे और नीचे जैतूनी-हरे या भूरे रंग की परत दिखाई दे सकती है।",
        "healthy_prevention": "पत्तियों की नियमित जाँच करें, मिट्टी में पानी दें और हवा आने-जाने दें।",
        "early_prevention": "रोगग्रस्त पत्तियाँ हटाएँ, पत्तियों को गीला करने से बचें और स्थानीय कृषि विशेषज्ञ की सलाह लें।",
        "late_prevention": "रोगग्रस्त पौधों के हिस्सों को सुरक्षित तरीके से हटाएँ, ऊपर से पानी देने से बचें और कृषि विशेषज्ञ से सलाह लें।",
        "mold_prevention": "खेत में हवा आने-जाने दें, पत्तियों को गीला न करें और कृषि विशेषज्ञ से सलाह लें।",
        "unknown_symptoms": "मॉडल इस परिणाम के लिए किसी ज्ञात रोग का विवरण नहीं दे सका।",
        "unknown_prevention": "साफ फोटो लें और पुष्टि के लिए स्थानीय कृषि अधिकारी से संपर्क करें।"
    },

    "mr": {
        "home": "मुख्यपृष्ठ",
        "predict": "पिकावरील रोग ओळखा",
        "workers": "शेतमजूर शोधा",
        "register": "मजुराची नोंदणी",
        "dashboard": "डॅशबोर्ड",
        "welcome": "AgriSahayak AI मध्ये आपले स्वागत आहे",
        "tagline": "प्रत्येक शेतकऱ्यासाठी स्मार्ट शेती सहाय्य",
        "hero_text": "पानाच्या फोटोवरून पिकावरील संभाव्य रोग ओळखा.",
        "get_started": "पिकावरील रोग ओळखा",
        "features": "आमच्या सेवा",
        "feature1": "AI द्वारे रोग ओळख",
        "feature1_text": "संभाव्य रोग तपासण्यासाठी पानाचा फोटो अपलोड करा.",
        "feature2": "शेतमजूर शोधा",
        "feature2_text": "शेतीच्या कामासाठी मजूर शोधा.",
        "feature3": "वापरण्यास सोपे",
        "feature3_text": "शेतकऱ्यांसाठी सोपी आणि उपयुक्त साधने.",
        "language": "भाषा निवडा",
        "footer": "शेतकऱ्यांच्या चांगल्या शेतीसाठी मदत",
        "upload_title": "पिकावरील रोग ओळखा",
        "upload_text": "पिकाच्या पानाचा स्पष्ट फोटो अपलोड करा.",
        "choose_image": "पानाचा फोटो निवडा",
        "predict_button": "रोग ओळखा",
        "result": "ओळखीचा निकाल",
        "disease": "संभाव्य रोग",
        "confidence": "मॉडेलचा विश्वास स्तर",
        "symptoms": "सामान्य लक्षणे",
        "prevention": "प्रतिबंधक उपाय",
        "try_again": "दुसरा फोटो वापरा",
        "no_result": "रोग ओळखण्यासाठी पानाचा फोटो अपलोड करा.",
        "choose_error": "कृपया आधी फोटो निवडा.",
        "invalid_error": "JPG, JPEG, PNG किंवा WEBP फोटो वापरा.",
        "prediction_error": "माफ करा, फोटो तपासता आला नाही.",
        "healthy": "निरोगी पान",
        "early": "टोमॅटोवरील अर्ली ब्लाइट रोग",
        "late": "टोमॅटोवरील लेट ब्लाइट रोग",
        "leaf_mold": "टोमॅटोवरील लीफ मोल्ड रोग",
        "unknown": "अनोळखी रोग",
        "healthy_symptoms": "मॉडेलने कोणताही रोग ओळखलेला नाही. पिकाची नियमित तपासणी करत राहा.",
        "early_symptoms": "जुन्या पानांवर गडद डाग, वर्तुळाकार खुणा आणि पिवळेपणा दिसू शकतो.",
        "late_symptoms": "पानांवर पाणचट, गडद किंवा अनियमित डाग दिसू शकतात. ओलसर हवेत ते वेगाने पसरू शकतात.",
        "mold_symptoms": "पानांच्या वरच्या बाजूला पिवळे डाग आणि खालच्या बाजूला हिरवट-तपकिरी थर दिसू शकतो.",
        "healthy_prevention": "पानांची नियमित तपासणी करा, मातीला पाणी द्या आणि हवा खेळती ठेवा.",
        "early_prevention": "रोगग्रस्त पाने काढा, पानांवर पाणी पडणे टाळा आणि स्थानिक कृषी तज्ज्ञांचा सल्ला घ्या.",
        "late_prevention": "रोगग्रस्त भाग सुरक्षितपणे काढा, वरून पाणी देणे टाळा आणि कृषी तज्ज्ञांचा लवकर सल्ला घ्या.",
        "mold_prevention": "हवा खेळती ठेवा, पाने ओली होऊ देऊ नका आणि कृषी तज्ज्ञांचा सल्ला घ्या.",
        "unknown_symptoms": "या निकालासाठी मॉडेलला ओळखीच्या रोगाचे वर्णन देता आले नाही.",
        "unknown_prevention": "स्पष्ट फोटो घ्या आणि खात्रीसाठी स्थानिक कृषी अधिकाऱ्यांचा सल्ला घ्या."
    }
}


def tr(key):
    lang = session.get("lang", "mr")
    return TRANSLATIONS.get(lang, TRANSLATIONS["mr"]).get(
        key, TRANSLATIONS["en"].get(key, key)
    )


@app.context_processor
def inject_language():
    return {
        "lang": session.get("lang", "mr"),
        "languages": LANGUAGES,
        "tr": tr
    }


@app.route("/set-language/<language>")
def set_language(language):
    if language in LANGUAGES:
        session["lang"] = language
    return redirect(request.referrer or url_for("home"))


def get_db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = get_db()
    with open(BASE / "schema.sql", encoding="utf-8") as f:
        con.executescript(f.read())
    con.commit()
    con.close()


def load_model():
    if not MODEL_PATH.exists() or not CLASS_PATH.exists():
        return None, []
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(MODEL_PATH)
        classes = json.loads(CLASS_PATH.read_text(encoding="utf-8"))
        return model, classes
    except Exception as e:
        print("Model loading error:", e)
        return None, []


MODEL, CLASSES = load_model()


def get_disease_key(label):
    text = label.lower().replace("_", " ").replace("-", " ")

    if "early" in text:
        return "early"
    if "late" in text:
        return "late"
    if "leaf mold" in text or "leafmold" in text:
        return "leaf_mold"
    if "healthy" in text:
        return "healthy"
    return "unknown"


def make_result(label, confidence, demo=False):
    key = get_disease_key(label)
    lang = session.get("lang", "mr")
    words = TRANSLATIONS.get(lang, TRANSLATIONS["mr"])

    return {
        "label": words[key],
        "name": words[key],
        "confidence": confidence,
        "symptoms": words[key + "_symptoms"],
        "prevention": words[key + "_prevention"],
        "demo": demo
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/workers")
def workers():
    skill = request.args.get("skill", "").strip()
    location = request.args.get("location", "").strip()

    con = get_db()
    q = "SELECT * FROM workers WHERE 1=1"
    params = []

    if skill:
        q += " AND skill LIKE ?"
        params.append("%" + skill + "%")

    if location:
        q += " AND location LIKE ?"
        params.append("%" + location + "%")

    q += " ORDER BY rating DESC, experience_years DESC"
    rows = con.execute(q, params).fetchall()
    con.close()

    return render_template(
        "workers.html", workers=rows,
        skill=skill, location=location
    )


@app.route("/register-worker", methods=["GET", "POST"])
def register_worker():
    if request.method == "POST":
        con = get_db()
        con.execute(
            """INSERT INTO workers
            (name,phone,location,skill,experience_years,equipment,
             daily_rate,rating,available_days)
            VALUES(?,?,?,?,?,?,?,0,?)""",
            (
                request.form["name"],
                request.form["phone"],
                request.form["location"],
                request.form["skill"],
                int(request.form.get("experience_years", 0)),
                request.form.get("equipment", ""),
                float(request.form.get("daily_rate", 0)),
                request.form.get(
                    "available_days",
                    "Mon,Tue,Wed,Thu,Fri,Sat"
                )
            )
        )
        con.commit()
        con.close()

        flash(tr("success"))
        return redirect(url_for("workers"))

    return render_template("register_worker.html")


@app.route("/book/<int:worker_id>", methods=["POST"])
def book(worker_id):
    con = get_db()
    farmer = con.execute(
        "SELECT id FROM farmers ORDER BY id LIMIT 1"
    ).fetchone()

    if not farmer:
        con.execute(
            "INSERT INTO farmers(name,phone,location) VALUES(?,?,?)",
            ("Demo Farmer", "9999999999", "Pune")
        )
        con.commit()
        farmer = con.execute(
            "SELECT id FROM farmers ORDER BY id LIMIT 1"
        ).fetchone()

    con.execute(
        """INSERT INTO bookings
        (farmer_id,worker_id,work_type,booking_date,status)
        VALUES(?,?,?,?,?)""",
        (
            farmer["id"],
            worker_id,
            request.form["work_type"],
            request.form["booking_date"],
            "Pending"
        )
    )

    con.commit()
    con.close()

    flash(tr("booking"))
    return redirect(url_for("workers"))


@app.route("/predict", methods=["GET", "POST"])
def predict():
    result = None

    if request.method == "POST":
        file = request.files.get("image")

        if not file or file.filename == "":
            flash(tr("choose_error"))
            return redirect(url_for("predict"))

        ext = file.filename.rsplit(".", 1)[-1].lower()

        if ext not in ALLOWED:
            flash(tr("invalid_error"))
            return redirect(url_for("predict"))

        name = secure_filename(file.filename)
        path = UPLOADS / name
        file.save(path)

        if MODEL is not None and CLASSES:
            try:
                from PIL import Image

                with Image.open(path) as original:
                    img = original.convert("RGB").resize((224, 224))

                arr = np.array(img, dtype=np.float32) / 255.0
                pred = MODEL.predict(
                    np.expand_dims(arr, 0), verbose=0
                )[0]

                idx = int(np.argmax(pred))
                label = CLASSES[idx]
                confidence = round(float(pred[idx]) * 100, 2)

                result = make_result(label, confidence)

            except Exception as e:
                print("Prediction error:", e)
                result = {
                    "label": tr("prediction_error"),
                    "name": tr("prediction_error"),
                    "confidence": 0,
                    "symptoms": "",
                    "prevention": "",
                    "demo": True
                }
        else:
            result = {
                "label": "Model not trained yet",
                "name": "Model not trained yet",
                "confidence": 0,
                "symptoms": "",
                "prevention": "",
                "demo": True
            }

    return render_template("predict.html", result=result)


@app.route("/dashboard")
def dashboard():
    con = get_db()

    workers_count = con.execute(
        "SELECT COUNT(*) c FROM workers"
    ).fetchone()["c"]

    bookings_count = con.execute(
        "SELECT COUNT(*) c FROM bookings"
    ).fetchone()["c"]

    predictions_count = con.execute(
        "SELECT COUNT(*) c FROM predictions"
    ).fetchone()["c"]

    top = con.execute(
        """SELECT skill, COUNT(*) c FROM workers
        GROUP BY skill ORDER BY c DESC"""
    ).fetchall()

    con.close()

    return render_template(
        "dashboard.html",
        workers_count=workers_count,
        bookings_count=bookings_count,
        predictions_count=predictions_count,
        top=top
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
