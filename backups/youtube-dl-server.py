from __future__ import unicode_literals
import json
import os
import subprocess
from queue import Queue
# from bottle import route, run, Bottle, request, static_file
from threading import Thread
import youtube_dl
from pathlib import Path
from collections import ChainMap

# app = Bottle()

#!flask/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)


app_defaults = {
    'YDL_FORMAT': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
    'YDL_EXTRACT_AUDIO_FORMAT': None,
    'YDL_EXTRACT_AUDIO_QUALITY': '192',
    'YDL_RECODE_VIDEO_FORMAT': None,
    'YDL_OUTPUT_TEMPLATE': '/youtube-dl/%(title)s [%(id)s].%(ext)s',
    'YDL_ARCHIVE_FILE': None,
    'YDL_SERVER_HOST': '0.0.0.0',
    'YDL_SERVER_PORT': 8091,
}

# mediaFromat = 'bestaudio/best'

# @bottle.route('/youtube-dl/getVideoInfo', method='GET')
@app.route('/youtube-dl/getVideoInfo', methods=['GET'])
def get_video_info():
    video_url = request.args.get("videoURL")
    mediaCodec = request.args.get("mediaCodec")

    return __get_video_info(mediaCodec, video_url)

# @bottle.route('/youtube-dl/search', method='GET')
@app.route('/youtube-dl/search', methods=['GET'])
def search_youtube():
    searchText = request.args.get("searchText") or ''
    searchCount = request.args.get("searchCount") or 10
    mediaCodec = request.args.get("mediaCodec") or 'mp3'
    # mediaCodec = request.query.get("mediaCodec")
    medias = __search_youtube(searchText, searchCount, mediaCodec)

    return { "medias": medias }

def __get_video_info(mediaCodec, videoURL):
    # ydl_opts = {
    #     'format': 'bestvideo/best',
    #     'quiet': True,
    #     'no_warnings': True,
    #     'nocheckcertificate': True,
    #     'postprocessors': [{
    #         'key': 'FFmpegExtractAudio',
    #         'preferredcodec': mediaCodec,
    #         'preferredquality': '192',
    #     },
    #         {'key': 'FFmpegMetadata'},
    #     ],
    # }

    ydl_opts = get_ydl_options({'format': mediaCodec})
    ydl = youtube_dl.YoutubeDL(ydl_opts) 

    with ydl:
        result = ydl.extract_info(
            videoURL, # 'http://www.youtube.com/watch?v=gqOZIhgEqac',
            download=False, # We just want to extract the info
        )

    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result

    print(video)
    video_url = video['url']
    print(video_url)
    # return { "error": None, "response": { "url": video_url } }
    return video



def __search_youtube(searchText, searchCount, mediaCodec):
    ydl_opts = get_ydl_options({'format': 'mp4'})
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info("ytsearch" + str(searchCount) + ":" + searchText, download=False)
        if 'entries' in result:
            # Can be a playlist or a list of videos
            medias = result['entries']
        else:
            # Just a video
            medias = result

    return medias

# def dl_worker():
#     while not done:
#         url, options = dl_q.get()
#         # download(url, options)
#         dl_q.task_done()


def get_ydl_options(request_options):
    mediaFromat = 'bestaudio/best'

    request_vars = {
        'YDL_EXTRACT_AUDIO_FORMAT': None,
        'YDL_RECODE_VIDEO_FORMAT': None,
    }

    requested_format = request_options.get('format', 'bestvideo')

    if requested_format in ['aac', 'flac', 'mp3', 'm4a', 'opus', 'vorbis', 'wav']:
        request_vars['YDL_EXTRACT_AUDIO_FORMAT'] = requested_format
    elif requested_format == 'bestaudio':
        request_vars['YDL_EXTRACT_AUDIO_FORMAT'] = 'best'
    elif requested_format in ['mp4', 'flv', 'webm', 'ogg', 'mkv', 'avi']:
        request_vars['YDL_RECODE_VIDEO_FORMAT'] = requested_format

    ydl_vars = ChainMap(app_defaults)

    postprocessors = []

    if(ydl_vars['YDL_EXTRACT_AUDIO_FORMAT']):
        postprocessors.append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': ydl_vars['YDL_EXTRACT_AUDIO_FORMAT'],
            'preferredquality': ydl_vars['YDL_EXTRACT_AUDIO_QUALITY']
        })

        postprocessors.append({'key': 'FFmpegMetadata'})

        mediaFromat = 'bestaudio/best'

    if(ydl_vars['YDL_RECODE_VIDEO_FORMAT']):
        postprocessors.append({
            'key': 'FFmpegVideoConvertor',
            'preferedformat': ydl_vars['YDL_RECODE_VIDEO_FORMAT']
        })

        postprocessors.append({'key': 'FFmpegMetadata'})

        mediaFromat = 'bestvideo/best'

    return {
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'skip_download': True,
        'forceurl': True,
        'format': mediaFromat, #ydl_vars['YDL_FORMAT'],
        'postprocessors': postprocessors
        # 'outtmpl': ydl_vars['YDL_OUTPUT_TEMPLATE'],
        # 'download_archive': ydl_vars['YDL_ARCHIVE_FILE']
    }


# def download(url, request_options):
#     with youtube_dl.YoutubeDL(get_ydl_options(request_options)) as ydl:
#         ydl.download([url])

# app_vars = ChainMap(os.environ, app_defaults)



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port='8091', debug=True)

# app = bottle.default_app()
# from paste import httpserver
# httpserver.serve(app, host=app_vars['YDL_SERVER_HOST'], port=['YDL_SERVER_PORT'])

# dl_q = Queue()
# done = False
# dl_thread = Thread(target=dl_worker)
# dl_thread.start()

print("Started download thread")



# app.run(host=app_vars['YDL_SERVER_HOST'], port=app_vars['YDL_SERVER_PORT'], debug=True)
# done = True
# dl_thread.join()
