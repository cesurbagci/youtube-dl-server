from flask import Flask, Blueprint, request, jsonify
import os
import youtube_dl
from collections import ChainMap

# youtubeController = Blueprint('youtubeController', __name__)

youtube_defaults = {
    'YDL_FORMAT': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
    'YDL_EXTRACT_AUDIO_FORMAT': 'mp3',
    'YDL_EXTRACT_AUDIO_QUALITY': '192',
    'YDL_RECODE_VIDEO_FORMAT': None
}

app_vars = ChainMap(os.environ, youtube_defaults)

class youtubeDLController():
    @staticmethod
    def get_video_info(mediaCodec, videoURL):
        ydl_opts = youtubeDLController.get_ydl_options({'format': mediaCodec})
        ydl = youtube_dl.YoutubeDL(ydl_opts) 

        with ydl:
            ydl.add_default_info_extractors()
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
        
        video_url = video['url']
        video_title = ('' if video['artist'] == None else video['artist']) + ('' if video['track'] == None else ' - ' + video['track'])
        video_title = video['title'] if len(video_title) <= 1 else video_title
        video_title = video['id'] if len(video_title) <= 1 else video_title
        
        audioInfo = {
            'url': video_url,
            'title': video_title
        }
        # print(video_url)
        # return { "error": None, "response": { "url": video_url } }
        return audioInfo
        # return app.response_class(video, content_type='application/json')
        # return jsonify(video)
        # return app.response_class(video, content_type='application/json')


    @staticmethod
    def get_ydl_options(request_options):
        mediaFromat = 'bestaudio/best'

        request_vars = {
            'YDL_EXTRACT_AUDIO_FORMAT': None,
            'YDL_RECODE_VIDEO_FORMAT': None,
        }

        ydl_vars = dict(ChainMap(youtube_defaults))
        requested_format = request_options.get('format', 'bestvideo')

        if requested_format in ['aac', 'flac', 'mp3', 'm4a', 'opus', 'vorbis', 'wav']:
            request_vars['YDL_EXTRACT_AUDIO_FORMAT'] = requested_format
        elif requested_format == 'bestaudio':
            request_vars['YDL_EXTRACT_AUDIO_FORMAT'] = 'best'
        elif requested_format in ['mp4', 'flv', 'webm', 'ogg', 'mkv', 'avi']:
            request_vars['YDL_RECODE_VIDEO_FORMAT'] = requested_format

        postprocessors = []

        if(ydl_vars['YDL_EXTRACT_AUDIO_FORMAT']):
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': ydl_vars['YDL_EXTRACT_AUDIO_FORMAT'],
                'preferredquality': ydl_vars['YDL_EXTRACT_AUDIO_QUALITY']
            })

            # postprocessors.append({'key': 'FFmpegMetadata'})
            postprocessors.append({'key': 'FFmpegExtractAudio'})

            mediaFromat = 'bestaudio/best'

        if(request_vars['YDL_RECODE_VIDEO_FORMAT']):
            postprocessors.append({
                'key': 'FFmpegVideoConvertor',
                'preferedformat': ydl_vars['YDL_RECODE_VIDEO_FORMAT']
            })

            postprocessors.append({'key': 'FFmpegMetadata'})

            mediaFromat = 'bestvideo/best'

        return {
            'outtmpl': '%(title)s-%(id)s.%(ext)s',
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'skip_download': True,
            'forceurl': True,
            'format': mediaFromat, #ydl_vars['YDL_FORMAT'],
            'forcefilename': True,
            'forcetitle': True,
            'postprocessors': postprocessors,
            'consoletitle ': True
            # 'outtmpl': ydl_vars['YDL_OUTPUT_TEMPLATE'],
            # 'download_archive': ydl_vars['YDL_ARCHIVE_FILE']
        }
    @staticmethod
    def search(searchText, searchCount, mediaCodec):
        ydl_opts = youtubeDLController.get_ydl_options({'format': 'mp4'})
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info("ytsearch" + str(searchCount) + ":" + searchText, download=False)
            if 'entries' in result:
                # Can be a playlist or a list of videos
                medias = result['entries']
            else:
                # Just a video
                medias = result

        return medias