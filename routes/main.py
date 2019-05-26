from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
import os
import youtube_dl
from collections import ChainMap
from youtube.test import Todo
from youtube.test2 import TodoList

app = Flask(__name__)
api = Api(app)

app_defaults = {
    'YDL_FORMAT': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
    'YDL_EXTRACT_AUDIO_FORMAT': None,
    'YDL_EXTRACT_AUDIO_QUALITY': '192',
    'YDL_RECODE_VIDEO_FORMAT': None,
    'YDL_SERVER_HOST': '0.0.0.0',
    'YDL_SERVER_PORT': 8091,
}

app_vars = ChainMap(os.environ, app_defaults)

api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    app.run(host=app_defaults['YDL_SERVER_HOST'], port=app_defaults['YDL_SERVER_PORT'], debug=True)