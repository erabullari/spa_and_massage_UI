from flask_app.controller import users
from flask_app import app
from flask_app.config import mysqlconnection


if __name__ == "__main__":
    app.run(debug=True ,port=8000)