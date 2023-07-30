import os
import re

def process_srt_file(filename):
    with open(filename, 'r', encoding='utf8') as fp:
        lines = fp.readlines()

    new_lines = []
    i = 0
    while i < len(lines):
        if re.match(r'^\d+\n$', lines[i]):  # matches the index line (e.g., "1\n")
            new_lines.append(lines[i])
            i += 1
        elif re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n$', lines[i]):  # matches the time stamp line
            new_lines.append(lines[i])
            i += 1
        else:  # assuming this is the English and Chinese subtitle part
            eng_line = lines[i]
            chn_line = lines[i+1]
            new_lines.append(chn_line)  # switch the order
            new_lines.append(eng_line)
            i += 2
            if i < len(lines) and lines[i] == '\n':  # if there is a blank line, add it to new_lines
                new_lines.append(lines[i])
                i += 1
    return new_lines

def write_to_file(lines, filename):
    with open(filename, 'w', encoding='utf8') as fp:
        fp.writelines(lines)

if __name__ == "__main__":
    srt_files = [file for file in os.listdir("./") if file.endswith(".srt")]

    for srt_file in srt_files:
        processed_lines = process_srt_file(srt_file)
        output_file = 'Switched_' + srt_file
        write_to_file(processed_lines, output_file)
