from flask import Flask
from flask_cors import CORS

from routes.tekmovanja import tekmovanja_bp
from routes.tekmovalci import tekmovalci_bp
from routes.rezultati import rezultati_bp
from routes.auth import auth_bp
from routes.validacija import validacija_bp
from routes.primerjava import primerjava_bp
from routes.spremembe import spremembe_bp

app = Flask(__name__, static_folder="web_app", static_url_path="")
CORS(app)

app.register_blueprint(tekmovanja_bp)
app.register_blueprint(tekmovalci_bp)
app.register_blueprint(rezultati_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(validacija_bp)
app.register_blueprint(primerjava_bp)
app.register_blueprint(spremembe_bp)


@app.get("/")
def serve_web_app():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True)