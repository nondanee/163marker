# -*- coding: utf-8 -*-
import sys
import re, json, binascii, base64, hashlib, html

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from mutagen import mp3, flac, id3

meta_key = binascii.a2b_hex('2331346C6A6B5F215C5D2630553C2728')

def parse_event(url):
    id = re.search(r'id=(\d+)', url)[1]
    uid = re.search(r'uid=(\d+)', url)[1]
    response = requests.get('https://music.163.com/event', params = {'id': id, 'uid': uid})
    data = re.search(r'<textarea.+id="event-data".*>([\s\S]+?)</textarea>', response.text)[1]
    data = json.loads(html.unescape(data))
    song = json.loads(data['json'])['song']
    return song

def marker(path, song):
    def file_stream(file):
        with file:
            return file.read()

    def embed_cover(item, content, type):
        item.encoding = 0
        item.type = type
        item.mime = 'image/png' if content[0:4] == binascii.a2b_hex('89504E47') else 'image/jpeg'
        item.data = content
    
    meta = {
        'album': song['album']['name'],
        'albumId': song['album']['id'],
        'albumPic': song['album']['picUrl'],
        'albumPicDocId': song['album']['pic'],
        'alias': song['alias'],
        'artist': [[artist['name'], artist['id']] for artist in song['artists']],
        'musicId': song['id'],
        'musicName': song['name'],
        'mvId': song['mvid'],
        'transNames': [],
        'format': 'mp3'
    }

    audio = mp3.EasyMP3(path)
    meta['bitrate'] = audio.info.bitrate
    meta['duration'] = (int(audio.info.length * 1000))
    meta['mp3DocId'] = hashlib.md5(file_stream(open(path, 'rb'))).hexdigest()

    cryptor = AES.new(meta_key, AES.MODE_ECB)
    identification = 'music:' + json.dumps(meta)
    identification = '163 key(Don\'t modify):' + base64.b64encode(cryptor.encrypt(pad(identification.encode('utf8'), 16))).decode('utf8')

    audio['title'] = meta['musicName']
    audio['album'] = meta['album']
    audio['artist'] = '/'.join([artist[0] for artist in meta['artist']])
    audio.tags.RegisterTextKey('comment', 'COMM')
    audio['comment'] = identification
    audio.save()

    audio = mp3.MP3(path)
    image = id3.APIC()
    embed_cover(image, requests.get(meta['albumPic'] + '?param=300y300').content, 6)
    audio.tags.add(image)
    audio.save()

if __name__ == '__main__':
    try:
        marker(sys.argv[1], parse_event(sys.argv[2]))
    except Exception as e:
        print(e)