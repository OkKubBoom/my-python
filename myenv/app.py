from flask import Flask
from api.user import user_bp

app = Flask(__name__)

# ลงทะเบียน Blueprint ของ user
app.register_blueprint(user_bp)
@app.route('/')
def home():
    return "Home"
if __name__ == '__main__':
    app.run(debug=True)
