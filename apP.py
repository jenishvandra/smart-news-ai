from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = "secret123"

# Dummy user storage
users = {}

# Load news data
with open("news_data.json", "r", encoding="utf-8") as f:
    news_data = json.load(f)


# 🤖 AI RESPONSE
def get_ai_response(user_query: str) -> str:
    q = user_query.lower()

    responses = {
        "startup": news_data["startup"]["summary"],
        "stock": news_data["stock"]["summary"],
        "market": news_data["stock"]["summary"],
        "economy": news_data["economy"]["summary"],
        "inflation": news_data["economy"]["summary"],

        "ambulance": "🚑 Call 108 immediately for emergency ambulance service.",
        "emergency": "🚑 Dial 108 for emergency help.",
        "hospital": "🏥 Search nearby hospitals on Google Maps.",
        "police": "👮 Call 100 for police help.",
        "fire": "🔥 Call 101 for fire emergency."
    }

    for key in responses:
        if key in q:
            return responses[key]

    return "🤖 Sorry, I didn't understand. Try startup, stock, economy, emergency."

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":

        email = request.form.get("email")
        username = request.form.get("username")
        phone = request.form.get("phone")
        city = request.form.get("city")
        password = request.form.get("password")

        users[email] = {
            "username": username,
            "phone": phone,
            "city": city,
            "password": password,
            "skills": [],
            "work": []
        }

        return redirect("/")

    return render_template("signup.html")
# 🔐 LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if email in users and users[email]["password"] == password:

            session["email"] = email

            return redirect("/home")  # ✅ DASHBOARD

        return "❌ Invalid login"

    return render_template("login.html")
# profile
@app.route("/profile")
def profile():
    if "email" not in session:  # 🔴 "email" check karo
        return redirect("/")

    user = users.get(session["email"])

    return render_template(
        "profile.html",
        user=user,
        user_email=session["email"]
    )
# video news
@app.route("/video-news")
def video_news():
    return render_template("video_news.html")

# startups
@app.route("/startups")
def startups():
    return render_template("startups.html")

# Market
@app.route("/market")
def market():
    return render_template("market.html")

# My feed
@app.route("/my-feed")
def my_feed():
    return render_template("my_feed.html")
# read 
@app.route("/read")
def read():
    return render_template("read.html")

# Watch
@app.route("/watch")
def watch():
    return render_template("watch.html")

# 🏠 HOME PAGE
@app.route("/home")
def home():
    if "email" not in session:  # 🔴 "user" ki jagah "email" check karo
        return redirect(url_for("login"))

    return render_template("old.html", user=session.get("email"))


# 🤖 ASK AI
@app.route("/ask-ai", methods=["GET", "POST"])
def ask_ai():
    if "email" not in session:  # 🔴 "user" ki jagah "email" check karo
        return redirect(url_for("login"))

    if "chat" not in session:
        session["chat"] = []

    if request.method == "POST":
        user_msg = request.form.get("query")

        if user_msg:
            ai_reply = get_ai_response(user_msg)

            session["chat"].append({"type": "user", "msg": user_msg})
            session["chat"].append({"type": "ai", "msg": ai_reply})

            session.modified = True

    return render_template("ask_ai.html", chat=session["chat"])


# CLEAR CHAT
@app.route("/clear-chat")
def clear_chat():
    session["chat"] = []
    return redirect(url_for("ask_ai"))


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)