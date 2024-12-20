import os
import json
import subprocess
import asyncio

def book_code_to_short_title(code):
    if code == 'Song2':
        return 'Song of Songs'
    return code.replace('-', ' ')

book_code_to_title = {
    'Genesis': 'The Book of Genesis',
    'Exodus': 'The Book of Exodus',
    'Leviticus': 'The Book of Leviticus',
    'Numbers': 'The Book of Numbers',
    'Deuteronomy': 'The Book of Deuteronomy',
    'Joshua': 'The Book of Joshua',
    'Judges': 'The Book of Judges',
    'Ruth': 'The Book of Ruth',
    '1-Samuel': 'Samuel One',
    '2-Samuel': 'Samuel Two',
    '1-Kings': 'Kings One',
    '2-Kings': 'Kings Two',
    '1-Chronicles': 'Chronicles One',
    '2-Chronicles': 'Chronicles Two',
    'Ezra': 'The Book of Ezra',
    'Nehemiah': 'The Book of Nehemiah',
    'Tobit': 'The Book of Tobit',
    'Judith': 'The Book of Judith',
    'Esther': 'The Book of Esther',
    'Job': 'The Book of Job',
    'Psalms': 'The Book of Psalms',
    'Proverbs': 'The Book of Proverbs',
    'Ecclesiastes': 'The Book of Ecclesiastes',
    'Song2': 'Song of Songs',
    'Wisdom': 'The Book of Wisdom',
    'Sirach': 'The Book of Sirach',
    'Isaiah': 'The Book of Isaiah',
    'Jeremiah': 'The Book of Jeremiah',
    'Lamentations': 'The Book of Lamentations',
    'Baruch': 'The Book of Baruch',
    'Ezekiel': 'The Book of Ezekiel',
    'Daniel': 'The Book of Daniel',
    'Hosea': 'The Book of Hosea',
    'Joel': 'The Book of Joel',
    'Amos': 'The Book of Amos',
    'Obadiah': 'The Book of Obadiah',
    'Jonah': 'The Book of Jonah',
    'Micah': 'The Book of Micah',
    'Nahum': 'The Book of Nahum',
    'Habakkuk': 'The Book of Habakkuk',
    'Zephaniah': 'The Book of Zephaniah',
    'Haggai': 'The Book of Haggai',
    'Zechariah': 'The Book of Zechariah',
    'Malachi': 'The Book of Malachi',
    '1-Maccabees': 'First Maccabees',
    '2-Maccabees': 'Second Maccabees',
    'Matthew': 'The Gospel According to Matthew',
    'Mark': 'The Gospel According to Mark',
    'Luke': 'The Gospel According to Luke',
    'John': 'The Gospel According to John',
    'Acts': 'The Acts of the Apostles',
    'Romans': 'The Letter to The Romans',
    '1-Corinthians': 'The First Letter to The Corinthians',
    '2-Corinthians': 'The Second Letter to The Corinthians',
    'Galatians': 'The Letter to The Galatians',
    'Ephesians': 'The Letter to The Ephesians',
    'Philippians': 'The Letter to The Philippians',
    'Colossians': 'The Letter to The Colossians',
    '1-Thessalonians': 'The First Letter to The Thessalonians',
    '2-Thessalonians': 'The Second Letter to The Thessalonians',
    '1-Timothy': 'The First Letter to Timothy',
    '2-Timothy': 'The Second Letter to Timothy',
    'Titus': 'The Letter to Titus',
    'Philemon': 'The Letter to Philemon',
    'Hebrews': 'The Letter to the Hebrews',
    'James': 'The Letter from James',
    '1-Peter': 'The First letter from Peter',
    '2-Peter': 'The Second Letter from Peter',
    '1-John': 'The First Letter from John',
    '2-John': 'The Second Letter from John',
    '3-John': 'The Third Letter from John',
    'Jude': 'The Letter from Jude',
    'Revelation': 'The Book of Revelation',
}

json = json.load(open('EntireBible-CPDV.json', 'r'))

async def run_processing_commands(ffmpeg_command, chapter_text, eyed3_command):
    subprocess.run(ffmpeg_command)

    lyrics_file = open(eyed3_command[1] + '.txt', 'w')
    lyrics_file.write(chapter_text)
    lyrics_file.close()

    subprocess.run(eyed3_command)
    os.remove(ffmpeg_command[2])
    os.remove(eyed3_command[1] + '.txt')

def make_mp3(model, book_code, chapter_number):
    short_book_title = book_code_to_short_title(book_code)
    chapter_text = '. '.join(json[book_code][chapter_number].values()) + '.'
    chapter_text = chapter_text.replace('<I>', '').replace('</I>', '').replace('..', '.').replace('“', '"').replace('”', '"').replace('’', '\'').replace('‘', '\'')
    chapter_text =  book_code_to_title[book_code] + ' Chapter ' + chapter_number + '\r\r' + chapter_text
    wav_file_name = 'output/' + model + '/' + short_book_title + '/' + short_book_title + ' ' + chapter_number + '.wav'
    mp3_file_name = wav_file_name.replace('.wav', '.mp3')
    if os.path.exists(mp3_file_name):
        return
    piper_command = ['piper/piper', '--model', 'models/' + model + '.onnx', '--output_file', wav_file_name]
    subprocess.run(piper_command, input = chapter_text.replace('\r\r', '. '), text = True)

    ffmpeg_command = [
        'ffmpeg',
        '-i', wav_file_name,
        '-vn',
        '-ar', '22050',
        '-ac', '1',
        '-b:a', '40k',
        '-y',
        mp3_file_name
    ]

    eyed3_command = [
        'eyeD3',
        mp3_file_name,
        '--title', short_book_title + ' Chapter ' + chapter_number,
        '--artist', 'Ronald L. Conte Jr.',
        '--album', short_book_title,
        '--track', str(chapter_number),
        '--genre', 'Catholic Public Domain Version',
        '--add-lyrics', mp3_file_name + ".txt"
    ]
    asyncio.run(run_processing_commands(ffmpeg_command, chapter_text, eyed3_command))

if not os.path.isdir('output'):
    os.mkdir('output')

for model in os.listdir('models'):
    if not model.endswith('.onnx'):
        continue

    model = model.replace('.onnx', '')

    if not os.path.isdir('output/' + model):
        os.mkdir('output/' + model)

    for book_code in json:
        if type(json[book_code]) is str:
            continue

        book_dir = 'output/' + model + '/' + book_code_to_short_title(book_code)
        if not os.path.isdir(book_dir):
            os.mkdir(book_dir)

        for chapter_number in json[book_code]:
            make_mp3(model, book_code, chapter_number)
