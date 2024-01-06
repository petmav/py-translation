import re
import ast

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

def argument_identifier(args: list) -> list:

    final = []
    count = 0

    for arg in args:

        temp = arg.split('=', maxsplit=1)

        if count == 1:

            try:

                if type(ast.literal_eval(temp[1])) in [int, str, list, dict]:
                    raise Exception

                final.append(ast.literal_eval(temp[1]))
                print(f'Tuple/float for {temp[0]} found.')

            except Exception as e:

                final.append((0.0, 0.2, 0.4, 0.6, 0.8, 1.0))
                print(f'Tuple/float for {temp[0]} not found. Applied default.')

            count += 1
            continue

        if count == 19:

            try:

                if temp[1].lower() == 'none':

                    final.append(None)
                    count += 1
                    print(f'Dictionary for {temp[0]} not found. Applied default.')
                    continue

                final.append(ast.literal_eval(temp[1]))
                print(f'Dictionary for {temp[0]} found.')

            except Exception as e:

                final.append(None)
                print(f'Dictionary for {temp[0]} not found. Applied default.')

            count += 1
            continue

        try:
            converted_value = float(temp[1])
            if converted_value.is_integer():
                final.append(int(converted_value))
            else:
                final.append(converted_value)
        except ValueError:
            if temp[1].lower() in ['true', 'false', 'none']:
                if temp[1].lower() == 'true':
                    final.append(True)
                elif temp[1].lower() == 'false':
                    final.append(False)
                elif temp[1].lower() == 'none':
                    final.append(None)
            else:
                final.append(str(temp[1]))

        count += 1

    return final


def extract_and_filter_args() -> list:

    arguments_filtered = ['verbose=', 'temperature=', 'compression_ratio_threshold=', 'logprob_threshold=', 'no_speech_threshold=', 'condition_on_previous_text=', 'initial_prompt=', 'word_timestamps=', 'regroup=', 'ts_num=', 'ts_noise=', 'suppress_silence=', 'suppress_word_ts=', 'use_word_position=', 'q_levels=', 'k_size=', 'time_scale=', 'demucs=', 'demucs_output=', 'demucs_options=', 'vad=', 'vad_threshold=', 'vad_onnx=', 'min_word_dur=', 'nonspeech_error=', 'only_voice_freq=', 'prepend_punctuations=', 'append_punctuations=', 'mel_first=', 'split_callback=', 'suppress_ts_tokens=', 'gap_padding=', 'only_ffmpeg=', 'max_instant_words=', 'avg_prob_threshold=', 'progress_callback=', 'ignore_compatibility=']
    count = 0

    with open('settings/transcribe.txt', 'r', encoding='utf-8') as f:

        for line in f:

            temp = line.split('=', maxsplit=1)

            if len(temp[1]) < 1:

                continue

            arguments_filtered[count] = arguments_filtered[count] + temp[1].strip()
            count += 1

        f.close()

    return argument_identifier(arguments_filtered)

def finalize_arguments():

    with open('data/final_transcribe.txt', 'r', encoding='utf-8') as f:

        count = 0
        arguments_filtered = ['verbose=', 'temperature=', 'compression_ratio_threshold=', 'logprob_threshold=', 'no_speech_threshold=', 'condition_on_previous_text=', 'initial_prompt=', 'word_timestamps=', 'regroup=', 'ts_num=', 'ts_noise=', 'suppress_silence=', 'suppress_word_ts=', 'use_word_position=', 'q_levels=', 'k_size=', 'time_scale=', 'demucs=', 'demucs_output=', 'demucs_options=', 'vad=', 'vad_threshold=', 'vad_onnx=', 'min_word_dur=', 'nonspeech_error=', 'only_voice_freq=', 'prepend_punctuations=', 'append_punctuations=', 'mel_first=', 'split_callback=', 'suppress_ts_tokens=', 'gap_padding=', 'only_ffmpeg=', 'max_instant_words=', 'avg_prob_threshold=', 'progress_callback=', 'ignore_compatibility=']

        for line in f:

            temp = line.split('=', maxsplit=1)

            if len(temp[1]) < 1:

                continue

            arguments_filtered[count] = arguments_filtered[count] + temp[1].strip()
            count += 1

        f.close()

        x = argument_identifier(arguments_filtered)
        y = extract_and_filter_args()
        print(x)
        print(y)

        z = [y[i] if y[i] not in ['', None] else x[i] for i in range(len(x))]

        return z


if __name__ == '__main__':
    print('lol')
