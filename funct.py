import re


def srt_to_txt(srt_file_path, txt_file_path):
    with open(srt_file_path, 'r', encoding='utf-8') as srt:
        lines = srt.readlines()
    text = []
    for line in lines:
        if not re.match(r'(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})|(\d+)', line.strip()):
            text.append(line)
    with open(txt_file_path, "w", encoding='utf-8') as txt:
        txt.writelines(text)


def txt_to_srt_clean(txt_file_path, final_output):
    delete_list = ['<font color="#00ff00">', '</font>']
    with open(txt_file_path, 'r', encoding='utf-8') as fin, open(final_output, "w+", encoding='utf-8') as fout:
        for line in fin:
            for word in delete_list:
                line = line.replace(word, "")
            fout.write(line)


def remove_duplicate_lines(filename):
    lines_seen = set()
    outfile = open("final_text.txt", "w", encoding='utf-8')
    for line in open(filename, "r", encoding='utf-8'):
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()


def code_to_language(code):

    codes = ("af am ar as az ba be bg bn bo br bs ca cs cy da de el en es et eu fa fi fo fr gl gu ha haw he "
             "hi hr ht hu hy id is it ja jw ka kk km kn ko la lb ln lo lt lv mg mi mk ml mn mr ms mt my ne "
             "nl nn no oc pa pl ps pt ro ru sa sd si sk sl sn so sq sr su sv sw ta te tg th tk tl tr tt uk "
             "ur uz vi yi yo zh yue").split()

    languages = ['english', 'chinese', 'german', 'spanish', 'russian', 'korean', 'french', 'japanese', 'portuguese',
                 'turkish',
                 'polish', 'catalan', 'dutch', 'arabic', 'swedish', 'italian', 'indonesian', 'hindi', 'finnish',
                 'vietnamese',
                 'hebrew', 'ukrainian', 'greek', 'malay', 'czech', 'romanian', 'danish', 'hungarian', 'tamil',
                 'norwegian',
                 'thai', 'urdu', 'croatian', 'bulgarian', 'lithuanian', 'latin', 'maori', 'malayalam', 'welsh',
                 'slovak',
                 'telugu', 'persian', 'latvian', 'bengali', 'serbian', 'azerbaijani', 'slovenian', 'kannada',
                 'estonian',
                 'macedonian', 'breton', 'basque', 'icelandic', 'armenian', 'nepali', 'mongolian', 'bosnian', 'kazakh',
                 'albanian',
                 'swahili', 'galician', 'marathi', 'punjabi', 'sinhala', 'khmer', 'shona', 'yoruba', 'somali',
                 'afrikaans',
                 'occitan', 'georgian', 'belarusian', 'tajik', 'sindhi', 'gujarati', 'amharic', 'yiddish', 'lao',
                 'uzbek',
                 'faroese', 'haitian creole', 'pashto', 'turkmen', 'nynorsk', 'maltese', 'sanskrit', 'luxembourgish',
                 'myanmar',
                 'tibetan', 'tagalog', 'malagasy', 'assamese', 'tatar', 'hawaiian', 'lingala', 'hausa', 'bashkir',
                 'javanese',
                 'sundanese', 'cantonese']

    if code in codes:

        idx = codes.index(code)
        language = languages[idx]
        return language

    else:
        return False


def extract_microsoft():
    try:
        with open('settings/keys.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                index = line.find('MICROSOFT=')
                if index != -1:
                    _, string = line.split('=', maxsplit=1)
                    return string.strip()
            raise Exception("No 'MICROSOFT' key found in the file.")
    except FileNotFoundError:
        print("The file 'keys.txt' does not exist.")
        return


def extract_chatgpt():
    try:
        with open('settings/keys.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                index = line.find('CHATGPT=')
                if index != -1:
                    _, string = line.split('=', maxsplit=1)
                    return string.strip()
            raise Exception("No 'CHATGPT' key found in the file.")
    except FileNotFoundError:
        print("The file 'keys.txt' does not exist.")
        return

def extract_transcribe_args():

    arguments = {}

    with open('settings/transcribe.txt', 'r', encoding='utf-8') as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            if not key and value:
                continue
            else:
                arguments[key] = value

    return arguments