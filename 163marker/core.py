# -*- coding: utf-8 -*-
import os, re, json, binascii, base64, hashlib

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from mutagen import mp3, flac, id3

key = binascii.a2b_hex('2331346C6A6B5F215C5D2630553C2728')
headers = { 'X-Real-IP': '211.161.244.70', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36' }

def parse(uri):
    if 'event' in uri:
        id = re.search(r'id=(\d+)', uri).group(1)
        uid = re.search(r'uid=(\d+)', uri).group(1)
        response = requests.get('https://music.163.com/event', params = { 'id': id, 'uid': uid }, headers = headers)
        data = re.search(r'<textarea.+id="event-data".*>([\s\S]+?)</textarea>', response.text).group(1)
        data = json.loads(data.replace('&quot;', '"'))
        data = json.loads(data['json'])
        if 'song' in data:
            return data['song']
        elif 'resource' in data:
            return json.loads(data['resource']['resourceInfo'])
        elif 'event' in data:
            data = json.loads(data['event']['json'])
            if 'song' in data:
                return data['song']
            elif 'resource' in data:
                return json.loads(data['resource']['resourceInfo'])
    elif 'album' in uri:
        id = re.search(r'id=(\d+)', uri).group(1)
        response = requests.get('https://music.163.com/api/album/' + id, headers = headers)
        data = json.loads(response.text)
        return {
            'album': data['album'],
            'artists': data['album']['artists']
        }
    elif 'song' in uri:
        id = re.search(r'id=(\d+)', uri).group(1)
        response = requests.get('https://music.163.com/api/song/detail?ids=[' + id + ']', headers = headers)
        data = json.loads(response.text)
        return data['songs'][0]
    elif os.path.exists(uri):
        data = extract(uri)
        return {
            'album': {
                'name': data['album'],
                'id': data['albumId'],
                'picUrl': data['albumPic']
            },
            'artists': [{ 'name': artist[0], 'id': artist[1] } for artist in data['artist']]
        }

def mark(path, song, id = None):
    def streamify(file):
        with file:
            return file.read()

    def embed(item, content, type):
        item.encoding = 0
        item.type = type
        item.mime = 'image/png' if content[0:4] == binascii.a2b_hex('89504E47') else 'image/jpeg'
        item.data = content

    format = 'flac' if open(path, 'rb').read(4) == binascii.a2b_hex('664C6143') else 'mp3'
    audio = mp3.EasyMP3(path) if format == 'mp3' else flac.FLAC(path)

    meta = {
        'album': song['album']['name'],
        'albumId': song['album']['id'],
        'albumPic': song['album']['picUrl'],
        'albumPicDocId': str(song['album']['pic'] if 'pic' in song['album'] else re.search(r'/(\d+)\.\w+$', song['album']['picUrl']).group(1)),
        'alias': song['alias'] if 'alias' in song else [],
        'artist': [[artist['name'], artist['id']] for artist in song['artists']],
        'musicId': id if id else song['id'],
        'musicName': song['name'] if 'name' in song else audio['title'][0],
        'mvId': song['mvid'] if 'mvid' in song else 0,
        'transNames': [],
        'format': format,
        'bitrate': audio.info.bitrate,
        'duration': int(audio.info.length * 1000),
        'mp3DocId': hashlib.md5(streamify(open(path, 'rb'))).hexdigest()
    }

    cryptor = AES.new(key, AES.MODE_ECB)
    identifier = 'music:' + json.dumps(meta)
    identifier = '163 key(Don\'t modify):' + base64.b64encode(cryptor.encrypt(pad(identifier.encode('utf8'), 16))).decode('utf8')

    audio.delete()
    audio['title'] = meta['musicName']
    audio['album'] = meta['album']
    audio['artist'] = '/'.join([artist[0] for artist in meta['artist']])

    if format == 'flac':
        audio['description'] = identifier
    else:
        audio.tags.RegisterTextKey('comment', 'COMM')
        audio['comment'] = identifier
    audio.save()

    data = requests.get(meta['albumPic'] + '?param=300y300').content
    if format == 'flac':
        audio = flac.FLAC(path)
        image = flac.Picture()
        embed(image, data, 3)
        audio.clear_pictures()
        audio.add_picture(image)
    elif format == 'mp3':
        audio = mp3.MP3(path)
        image = id3.APIC()
        embed(image, data, 6)
        audio.tags.add(image)
    audio.save()

def extract(path):
    if open(path, 'rb').read(4) == binascii.a2b_hex('664C6143'):
        audio = flac.FLAC(path)
        identifier = audio['description']
    else:
        audio = mp3.MP3(path)
        identifier = [text for item in audio.tags.getall('COMM') for text in item.text]
    identifier = max(identifier, key = len)

    identifier = base64.b64decode(identifier[22:])
    cryptor = AES.new(key, AES.MODE_ECB)
    meta = unpad(cryptor.decrypt(identifier), 16).decode('utf8')
    return json.loads(meta[6:])
