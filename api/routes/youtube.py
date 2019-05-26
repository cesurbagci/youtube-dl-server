from flask import Flask, Blueprint, request, jsonify, json
from controllers.youtube import youtubeController

youtube = Blueprint('youtube', __name__)


@youtube.route('/')
def index():
    return "Youtube"

@youtube.route('/getVideoInfo', methods=['GET'])
def get_video_info():
    video_url = request.args.get("videoURL")
    mediaCodec = request.args.get("mediaCodec")

    result = youtubeController.get_video_info(mediaCodec, video_url)
    headers = {
    }
    return jsonify(result), 200, headers


@youtube.route('/search', methods=['GET'])
def search():
    searchText = request.args.get("searchText") or ''
    searchCount = request.args.get("searchCount") or 10
    mediaCodec = request.args.get("mediaCodec") or 'mp3'
    # mediaCodec = request.query.get("mediaCodec")
    
    medias = youtubeController.search(searchText, searchCount, mediaCodec)
    result = { "medias": medias }
    headers = {
    }
    return jsonify(result), 200, headers