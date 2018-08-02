#!/usr/bin/python
#coding: utf-8
import pystrix
from pystrix.agi.core import *
from config import *
from yandex import get_file, get_text

def getFirstname(agi):
    uniqueID = agi.execute(GetVariable('UNIQUEID'))
    filename = generate_path + '/record' + uniqueID 

    agi.execute(StreamFile(get_file('Назовите ваше имя:')))
    agi.execute(RecordFile(filename, format='wav', escape_digits='', timeout=5000, sample_offset=0, beep=False, silence=2))
    textName = get_text(filename + '.wav', topic='names')

    agi.execute(StreamFile(get_file('Подтвердите правильность ввода вашего имени.')))
    agi.execute(StreamFile(get_file('Ваше имя: ' + textName + '. Ответьте Да или Нет. ')))
    agi.execute(RecordFile(filename, format='wav', escape_digits='', timeout=3000, sample_offset=0, beep=False, silence=2))
    text = get_text(filename + '.wav', topic='buying')
    if text == 'да':
        return textName
    else:
        return False 

def GetText(agi, question, ask, askname):
    uniqueID = agi.execute(GetVariable('UNIQUEID'))
    filename = generate_path + '/record' + uniqueID 

    agi.execute(StreamFile(get_file(question)))
    agi.execute(RecordFile(filename, format='wav', escape_digits='', timeout=5000, sample_offset=0, beep=False, silence=2))
    textName = get_text(filename + '.wav', topic='names')
    if textName == '':
        return False
    agi.execute(StreamFile(get_file(ask)))
    agi.execute(StreamFile(get_file(askname + textName + '. Ответьте Да или Нет. ')))
    agi.execute(RecordFile(filename, format='wav', escape_digits='', timeout=3000, sample_offset=0, beep=False, silence=2))
    text = get_text(filename + '.wav', topic='buying')
    if text == 'да':
        return textName
    else:
        return False 

if __name__ == '__main__':
    agi = pystrix.agi.AGI()
    agi.execute(Answer())

    uniqueID = agi.execute(GetVariable('UNIQUEID'))

    name = GetText(agi,'Назовите вашу фамилию:','Подтвердите правильность распознования фамилии.','Ваша фамилия: ')
    secondname = GetText(agi,'Назовите ваше имя:','Подтвердите правильность ввода вашего имени.','Ваше имя: ')

    agi.execute(StreamFile(get_file('Добрый день ' + name + ' ' + secondname)))

    agi.execute(Hangup())

