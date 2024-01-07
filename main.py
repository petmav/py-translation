import stable_whisper
import os
import time
import sys
import funct
import deep_translator

chatgpt_api = funct.extract_chatgpt()
microsoft_api = funct.extract_microsoft()
print(f'\nYour Microsoft Translator API key is: {microsoft_api}')
print(f'Your ChatGPT API key is: {chatgpt_api}')

languages_accepted = ("af am ar as az ba be bg bn bo br bs ca cs cy da de el en es et eu fa fi fo fr gl gu ha haw he "
                      "hi hr ht hu hy id is it ja jw ka kk km kn ko la lb ln lo lt lv mg mi mk ml mn mr ms mt my ne "
                      "nl nn no oc pa pl ps pt ro ru sa sd si sk sl sn so sq sr su sv sw ta te tg th tk tl tr tt uk "
                      "ur uz vi yi yo zh yue").split()

while True:

    model_selection = input(f'\nWelcome to the py-translation tool!\n'
                            f'Type [help] to see instructions on how to use the program.\n'
                            f'Type [tiny/base/small/medium/large] to choose a model.\n'
                            f'You can type [exit] to cancel the program.\n\n').lower()

    match model_selection:
        case "exit":

            sys.exit()

        case "help":

            print('\nThis program is utilised to transcribe and translate a video through the use of the OpenAI Whisper '
                  'model.\n'
                  'To use this model, type [tiny/base/small/medium/large] to choose a model and initiate the process.\n'
                  'After this, you will need the file (mp3/flac/wav extensions accepted) and the language being '
                  'translated.')

            time.sleep(3)

        case "tiny" | "base" | "small" | "medium" | "large":

            x = True

            while x:

                file_path = input('Model selected. Insert filename: ')
                file_path = f'inputs/{file_path.strip()}'

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

                if language == '':

                    print('Language has defaulted to auto-recognition.')
                    print(f'Running Whisper with parameters: {model_selection}, {file_path}, auto')
                    arguments = funct.finalize_arguments()
                    model = stable_whisper.load_faster_whisper(f'{model_selection}')
                    result = model.transcribe_stable(beam_size=int(arguments[0]), best_of=int(arguments[1]),
                                                     patience=float(arguments[2]),
                                                     length_penalty=float(arguments[3]),
                                                     repetition_penalty=float(arguments[4]),
                                                     no_repeat_ngram_size=int(arguments[5]), temperature=arguments[6],
                                                     compression_ratio_threshold=float(arguments[7]),
                                                     log_prob_threshold=float(arguments[8]),
                                                     no_speech_threshold=float(arguments[9]),
                                                     condition_on_previous_text=bool(arguments[10]),
                                                     prompt_reset_on_temperature=float(arguments[11]),
                                                     initial_prompt=arguments[12], prefix=str(arguments[13]),
                                                     suppress_blank=bool(arguments[14]),
                                                     suppress_tokens=list(arguments[15]),
                                                     without_timestamps=bool(arguments[16]),
                                                     max_initial_timestamp=float(arguments[17]),
                                                     word_timestamps=bool(arguments[18]),
                                                     prepend_punctuations=str(arguments[19]),
                                                     append_punctuations=str(arguments[20]),
                                                     vad_filter=bool(arguments[21]),
                                                     vad_parameters=arguments[22], audio=file_path, language=language)
                    x = False

                if language not in languages_accepted:

                    print('Language not valid. Please try again.')
                    continue

                if language in languages_accepted:

                    print(f'Running Whisper with parameters: {model_selection}, {file_path}, {language}')
                    model = stable_whisper.load_faster_whisper(f'{model_selection}')
                    arguments = funct.finalize_arguments()
                    result = model.transcribe_stable(beam_size=int(arguments[0]), best_of=int(arguments[1]), patience=float(arguments[2]),
                                                     length_penalty=float(arguments[3]), repetition_penalty=float(arguments[4]),
                                                     no_repeat_ngram_size=int(arguments[5]), temperature=arguments[6],
                                                     compression_ratio_threshold=float(arguments[7]),
                                                     log_prob_threshold=float(arguments[8]), no_speech_threshold=float(arguments[9]),
                                                     condition_on_previous_text=bool(arguments[10]),
                                                     prompt_reset_on_temperature=float(arguments[11]),
                                                     initial_prompt=arguments[12], prefix=str(arguments[13]),
                                                     suppress_blank=bool(arguments[14]), suppress_tokens=list(arguments[15]),
                                                     without_timestamps=bool(arguments[16]),
                                                     max_initial_timestamp=float(arguments[17]), word_timestamps=bool(arguments[18]),
                                                     prepend_punctuations=str(arguments[19]),
                                                     append_punctuations=str(arguments[20]), vad_filter=bool(arguments[21]),
                                                     vad_parameters=arguments[22], audio=file_path, language=language)

                    x = False

            result.to_srt_vtt('output.srt')

            funct.srt_to_txt('output.srt', "plain_text_output.txt")
            funct.txt_to_srt_clean('plain_text_output.txt', 'final_text_output.txt')
            funct.remove_duplicate_lines('final_text_output.txt')

            os.remove('plain_text_output.txt')

            print('Converted to plaintext.')

            translate_ask = input('Do you want to translate to English (TRANSLATION LONG AND ALMOST UNUSABLE)? (y/n): ')

            if translate_ask.lower() == 'y':

                while True:

                    translated = ''

                    translation_method = input(
                        'Do you want to translate through [google]/[gpt]/[microsoft] translator? ')

                    if translation_method == 'google':

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

                    if translation_method == 'gpt' and not chatgpt_api == '':

                        with open('final_text.txt', 'r', encoding='utf-8') as f:

                            i = 1

                            for line in f:

                                u = deep_translator.ChatGptTranslator(api_key=chatgpt_api, target='english').translate(
                                    line)
                                print(i)
                                translated += f'{u}\n'
                                i += 1

                        with open('translated.txt', 'w', encoding='utf-8') as f:

                            f.write(translated)

                        break

                    if translation_method == 'microsoft' and not microsoft_api == '':

                        with open('final_text.txt', 'r', encoding='utf-8') as f:

                            i = 1

                            for line in f:

                                u = deep_translator.MicrosoftTranslator(api_key=microsoft_api, target='en').translate(
                                    line)
                                print(i)
                                translated += f'{u}\n'
                                i += 1

                        with open('translated.txt', 'w', encoding='utf-8') as f:

                            f.write(translated)

                        break

                    else:
                        print('Invalid input. Check API keys if utilising some services.')
                        continue

            else:
                sys.exit()

        case _:
            print('\nPlease select a valid option.\n')
