# api/server.py

from flask import Flask, request, send_file, abort
from .image_api import generate_image
import io

app = Flask(__name__)

@app.route("/user", methods=["GET"])
def generate():
    userid = request.args.get("userid")
    name = request.args.get("name")
    url = request.args.get("bot_url")

    if userid is None:
        abort(400, description="Missing 'userid'")
    image_data = generate_image(userid, name, url)
    return send_file(io.BytesIO(image_data), mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)