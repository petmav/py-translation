import re

def srt_to_txt(srt_file_path, txt_file_path):
    with open(srt_file_path, 'r', encoding='utf-8') as srt:
        lines = srt.readlines()
    text = []
    for line in lines:
        # Check if the line is not a timestamp or an SRT index number
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