# flask
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# env
from os.path import join, dirname
from dotenv import load_dotenv

# modules
from modules.agent import agent_module
from modules.app import app_module
from modules.auth import auth_module
from modules.customer import customer_module
from modules.task import task_module
from modules.product import product_module
from modules.planogram import planogram_module
from modules.profile import profile_module
from modules.admin import admin_module
from modules.company import company_module


app = Flask(__name__)
app.register_blueprint(agent_module, url_prefix='/agent')
app.register_blueprint(app_module, url_prefix='/app')
app.register_blueprint(auth_module, url_prefix='/auth')
app.register_blueprint(customer_module, url_prefix='/customer')
app.register_blueprint(planogram_module, url_prefix='/planogram')
app.register_blueprint(task_module, url_prefix='/task')
app.register_blueprint(product_module, url_prefix='/product')
app.register_blueprint(profile_module, url_prefix='/profile' )
app.register_blueprint(admin_module, url_prefix='/admin' )
app.register_blueprint(company_module, url_prefix='/company' )

# load env vars
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app.config.from_object("config")
CORS(app)
jwt = JWTManager(app)

# test route
@app.route("/test")
def test():
    return {"message":"wellcome"}
    
if __name__ == '__main__':

    from db import db
    db.init_app(app)
    app.run(debug=True)