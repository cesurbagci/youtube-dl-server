from flask import Flask, request, jsonify
import os
import youtube_dl
from collections import ChainMap

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

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/youtube-dl/getVideoInfo', methods=['GET'])
def get_video_info():
    video_url = request.args.get("videoURL")
    mediaCodec = request.args.get("mediaCodec")

    return __get_video_info(mediaCodec, video_url)


def __get_video_info(mediaCodec, videoURL):
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

    # return { "error": None, "response": { "url": video_url } }
    # return video
    # return app.response_class(video, content_type='application/json')
    return jsonify(video)

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


app_vars = ChainMap(os.environ, app_defaults)

if __name__ == '__main__':
    app.run(host=app_defaults['YDL_SERVER_HOST'], port=app_defaults['YDL_SERVER_PORT'], debug=True)