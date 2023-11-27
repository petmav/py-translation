import stable_whisper
import faster_whisper
import os
import time
import sys
import funct
import deep_translator

languages_accepted = ("af am ar as az ba be bg bn bo br bs ca cs cy da de el en es et eu fa fi fo fr gl gu ha haw he "
                      "hi hr ht hu hy id is it ja jw ka kk km kn ko la lb ln lo lt lv mg mi mk ml mn mr ms mt my ne "
                      "nl nn no oc pa pl ps pt ro ru sa sd si sk sl sn so sq sr su sv sw ta te tg th tk tl tr tt uk "
                      "ur uz vi yi yo zh yue").split()

while True:
    print(f'Welcome to the py-translation tool!\n'
          f'Type [help] to see instructions on how to use the program.\n'
          f'Type [tiny/base/small/medium/large] to choose a model.\n'
          f'You can type [exit] to cancel the program.\n')

    model_selection = input()

    if model_selection == 'exit':
        sys.exit()

    if model_selection == 'help':
        print('This program is utilised to subtitle a video through the use of the OpenAI Whisper model.\n'
              'To use this model, type [tiny/base/small/medium/large] to choose a model and initiate the process.\n'
              'After this, you will need the file (mp3/flac/wav extensions accepted) and the language being '
              'translated.\n')
        time.sleep(3)
        continue

    elif model_selection == 'tiny' or model_selection == 'base' or model_selection == 'small' or model_selection == 'medium' or model_selection == 'large':

        x = True

        while x:
            file_path = input('Model selected. Insert file path: ')

            file_exists = os.path.isfile(file_path)
            file_extension = os.path.splitext(file_path)[1]

            if not file_exists:
                print('File does not exist. Please try again.')
                continue
            elif file_extension not in ['.mp3', '.flac', '.wav']:
                print('File extension is not valid. Please try again.')
                continue

            elif file_exists and file_extension in ['.mp3', '.flac', '.wav']:
                x = False

        x = True

        while x:
            language = input('File found. Insert language code (can be found in languages.txt): ')

            if language not in languages_accepted:
                print('Language not valid. Please try again.')
                continue

            if language in languages_accepted:
                print(f'Running Whisper with parameters: {model_selection}, {file_path}, {language}')
                x = False

        model = stable_whisper.load_faster_whisper(f'{model_selection}')
        result = model.transcribe_stable(file_path, language=language)

        result.to_srt_vtt('output.srt')

        funct.srt_to_txt('output.srt', "plain_text_output.txt")
        funct.txt_to_srt_clean('plain_text_output.txt', 'final_text_output.txt')
        funct.remove_duplicate_lines('final_text_output.txt')

        os.remove('plain_text_output.txt')

        print('Converted to plaintext.')

        translate_ask = input('Do you want to translate to English (TRANSLATION LONG AND ALMOST UNUSABLE)? (y/n): ')

        if translate_ask == 'y':

            while True:

                translation_method = input('Do you want to translate through [google] translator? ')

                if translation_method == 'google':

                    translated = ''

                    with open('final_text.txt', 'r', encoding='utf-8') as f:
                        i = 1
                        for line in f:
                            u = deep_translator.GoogleTranslator(source='auto', target='en').translate(line)
                            print(i)
                            translated += f'{u}\n'
                            i += 1

                    with open('translated.txt', 'w', encoding='utf-8') as f:
                        f.write(translated)

                    break

                else:
                    print('Invalid input.')
                    continue


        else:
            sys.exit()

    else:
        print('\nPlease select a valid option.\n')
        continue
