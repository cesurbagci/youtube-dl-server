from flask import Flask
from api.routes.youtube import youtube
# from bookshelf.admin.controllers import admin

app = Flask(__name__)

app.register_blueprint(youtube, url_prefix='/music')
# app.register_blueprint(admin, url_prefix='/admin')