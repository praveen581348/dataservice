from flask import Flask, render_template, request, redirect, flash
from redis_client import get_messages_from_redis, cache_message
from mysql_client import get_all_ids, get_message_by_id
from mongo_client import save_to_mongo

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

@app.route("/", methods=["GET"])
def index():
    try:
        all_ids = get_all_ids()
    except Exception as e:
        flash(f"MySQL error: {e}", "danger")
        all_ids = []
    return render_template("index.html", all_ids=all_ids, message=None)

@app.route("/search", methods=["POST"])
def search():
    msg_id = request.form["msg_id"]
    message = None
    source = None

    try:
        # First check Redis
        redis_messages = get_messages_from_redis()
        message = next((m for m in redis_messages if str(m["id"]) == msg_id), None)
        source = "Redis"

        # If not in Redis, check MySQL
        if not message:
            message = get_message_by_id(msg_id)
            if message:
                cache_message(message)
                source = "MySQL"
    except Exception as e:
        flash(f"Error during search: {e}", "danger")

    try:
        all_ids = get_all_ids()
    except:
        all_ids = []

    if message:
        message["source"] = source
    else:
        flash("Message not found in Redis or MySQL", "warning")

    return render_template("index.html", all_ids=all_ids, message=message)

@app.route("/submit", methods=["POST"])
def submit():
    msg_id = request.form["msg_id"]
    content = request.form["content"]
    received_at = request.form["received_at"]
    try:
        save_to_mongo({
            "id": msg_id,
            "content": content,
            "received_at": received_at
        })
        flash("Message submitted to MongoDB successfully.", "success")
    except Exception as e:
        flash(f"MongoDB submission failed: {e}", "danger")
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8013)

