from flask import Flask

from routes.tekmovanja import tekmovanja_bp
from routes.tekmovalci import tekmovalci_bp
from routes.rezultati import rezultati_bp
from routes.auth import auth_bp
from routes.validacija import validacija_bp
from routes.primerjava import primerjava_bp

app = Flask(__name__)

app.register_blueprint(tekmovanja_bp)
app.register_blueprint(tekmovalci_bp)
app.register_blueprint(rezultati_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(validacija_bp)
app.register_blueprint(primerjava_bp)

if __name__ == "__main__":
    app.run(debug=True)