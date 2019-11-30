from flask import Flask, Blueprint, request, jsonify, json
from controllers.youtube_dl_wrapper import youtubeDLController
import datetime

youtube = Blueprint('youtube', __name__)

class AppData:
    getInfoMusicCount = 0
    getInfoErrorCount = 0

@youtube.route('/')
# def index():
#     return "Youtubesfds"

# @youtube.route('/getInfo', methods=['GET'])
@youtube.route('/')
def get_video_info():
    video_url = request.args.get("audioURL")
    mediaCodec = 'm4a'  #request.args.get("mediaCodec")

    # for i in range(1000):
        # print(str(i) + "\n")
# {"error":null,"result":{"url":"https://r5---sn-hgn7rn7r.googlevideo.com/videoplayback?expire=1574999139&ei=A0DgXeOoBImE1gLKxIbwCg&ip=46.196.89.17&id=o-AAVdBTxGuSMLRTVO7ddCPUsckHVYhsA55vhP82aPCFZi&itag=18&source=youtube&requiressl=yes&mm=31%2C26&mn=sn-hgn7rn7r%2Csn-hpa7znsz&ms=au%2Conr&mv=m&mvi=4&pl=24&initcwndbps=942500&mime=video%2Fmp4&gir=yes&clen=10780269&ratebypass=yes&dur=205.659&lmt=1555601901720044&mt=1574977461&fvip=5&fexp=23842630&c=WEB&txp=5531432&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cmime%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&lsparams=mm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AHylml4wRQIhAICV8F5LFAj-hoGdWm8CzqzxCOW6YXAyw3f06ZhnpPjyAiAPsYLfXJE0f1pOUBXeSuEmlUfv2vjUMKJUHs3-vBULZA%3D%3D&sig=ALgxI2wwRQIhAN2RoMaX4PI5bffiqMjVsKSsrhP8cQmGMFC_9BnmMQ2MAiB-qVeRr-Zyu6dAzM4AEyXkXFYwMELd986sGqDF5D2CHQ%3D%3D","title":"Zeynep Bastık - Cesaretsizce Olmuyor Akustik (Jabbar Cover)"},"systemMeta":{"hostName":"MacBook-Pro-4.local","serverTimeInterval":1574977540,"serverTime":"29-11-2019 00:45:40 +03:00","serverTimeUTC":"28-11-2019 21:45:40 +00:00"}}

    result = {

    }

    try:
        audio_info = youtubeDLController.get_video_info(mediaCodec, video_url)
        result = {
            'error': None,
            'serverTime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'result': audio_info 
        }
        AppData.getInfoMusicCount += 1
        print(audio_info['url'])
        print(audio_info['title'])
        print("getInfoMusicCount: ", str(AppData.getInfoMusicCount) + " - Success")
        print("getInfoErrorCount: ", str(AppData.getInfoErrorCount))
    except Exception as err:
        result = {
            'error': str(err),
            'serverTime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'result': None 
        }
        AppData.getInfoErrorCount += 1
        print("error: ", str(err))
        print("getInfoMusicCount: ", str(AppData.getInfoMusicCount))
        print("getInfoErrorCount: ", str(AppData.getInfoErrorCount) + " - Error")
        # print("\n\n\n\n")
    # result = youtubeDLController.get_video_info(mediaCodec, video_url)
    headers = {
    }

    # musicDownloadInfo = {
    #     url: resu.url,
    #     title: info.title
    # }
    # print(result)

    

    return jsonify(result), 200, headers


@youtube.route('/search', methods=['GET'])
def search():
    searchText = request.args.get("searchText") or ''
    searchCount = request.args.get("searchCount") or 10
    mediaCodec = request.args.get("mediaCodec") or 'mp3'
    # mediaCodec = request.query.get("mediaCodec")
    
    medias = youtubeDLController.search(searchText, searchCount, mediaCodec)
    result = { "medias": medias }
    headers = {
    }
    return jsonify(result), 200, headers