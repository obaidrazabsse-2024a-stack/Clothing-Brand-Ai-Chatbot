from flask import Flask, request, jsonify
from faq import check_faq
from ai_service import get_ai_reply

app = Flask(__name__)

# =========================
# HEALTH CHECK (GUI NEEDS THIS)
# =========================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online"}), 200


# =========================
# CHAT ENDPOINT
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."})

    # 1️⃣ Check FAQ first
    faq_reply = check_faq(user_message)
    if faq_reply:
        return jsonify({"reply": faq_reply})

    # 2️⃣ AI fallback
    ai_reply = get_ai_reply(user_message)
    return jsonify({"reply": ai_reply})


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    print("🚀 Flask backend running...")
    app.run(host="127.0.0.1", port=5000, debug=True)
