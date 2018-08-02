#!/usr/bin/python
# coding:utf-8
import urllib
import os
import commands
import requests
from hashlib import sha256 as codingname
from config import *
from xml.dom import minidom


def _generate_url_pay(text, audio_format, speaker, key, **a):
    """
    Генерация ссылки на скачивания файла
    Платное
    """
    url = 'https://tts.voicetech.yandex.net/generate?' \
          'text={text}&' \
          'format={audio_format}&' \
          'lang=ru-RU&' \
          'speaker={speaker}&' \
          'speed=0.8&' \
          'key={key}'

    text = urllib.quote(text)

    url = url.format(
        text=text,
        audio_format=audio_format,
        speaker=speaker,
        key=key
    )

    return url


def _generate_url_free(text, audio_format, speaker, key, **a):
    """
    Генерация ссылки на скачивания файла
    Бесплатное
    """
    url = 'http://tts.voicetech.yandex.net/tts?' \
          'format={audio_format}&' \
          'quality=lo&platform=web&application=translate&lang=ru_RU&' \
          'speaker={speaker}&' \
          'speed=0.8&' \
          'text={text}'

    text = urllib.quote(text)

    url = url.format(
        text=text,
        audio_format=audio_format,
        speaker=speaker,
        key=key
    )

    return url


generate_url = _generate_url_free


def get_file(text, speaker=speaker, key=key, path=generate_path):
    url = generate_url(text, 'wav', speaker, key)
    filename = path + '/' + codingname(text + speaker).hexdigest()

    if not os.path.exists(filename + '.alaw') and len(text) > 0:
        file = open(filename + '.wav', 'wb')
		
		r = requests.get(url)
		if r.status_code == 200:
			file.write(r.content)
			file.close()
		
        #TODO change method of transcoding
        cmd = 'sox -V {fname}.wav -r 8000 -c 1 -t al {fname}.alaw vol 2'.format(fname=filename)
        commands.getoutput(cmd)
        commands.getoutput('rm -f {fname}.wav'.format(fname=filename))
    elif(len(text) == 0):
        return 'silence/1'
    return filename

def get_text(filename, key=key, topic='queries', audioformat='audio/x-wav'):
    #names
    #buying
    url = 'http://asr.yandex.net/asr_xml?' \
          'uuid={uuid}&' \
          'key={key}&' \
          'topic={topic}&' \
          'lang=Ru-ru&' \
          'disableAntimat=False'.format(key=key,topic=topic,uuid='01ae13cb555558b58fb536d496daa1e6')
    headers = {'Content-Type': audioformat}

    if os.path.exists(filename):
        files = {'file': open(filename, 'rb')}

        r = requests.post(url, headers=headers, data=files['file'])
        if r.status_code == requests.codes.ok:
            xmldoc = minidom.parseString(r.text.encode('utf-8'))
            itemlist = xmldoc.getElementsByTagName('variant')
            if len(itemlist):
                name = getText(itemlist[0].childNodes)
                return name.encode('utf-8')
    return ''

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

if __name__ == '__main__':
    print('No main')