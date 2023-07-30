import os
import re


def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


def convert_sub_to_arr(filename):
    with open(filename, 'r') as fp:
        subtitle = fp.read()
        subtitle = subtitle.replace("，",'  ').replace('。','')
        subtitle = subtitle.split('\n')
        for i in range(len(subtitle)):
            subtitle[i] = subtitle[i].lstrip()
    return subtitle

def is_chinese(char):
    if '\u4e00' <= char <= '\u9fa5':
        return True
    else:
        return False

def is_alphabet(char):
    if ('\u0041' <= char <= '\u005a') or ('\u0061' <= char <= '\u007a'):
        return True
    else:
        return False

def is_timeline(string):
    pattern = '(\d+.\d+.\d+.\d{3}).....(\d+.\d+.\d+.\d{3})'
    result = re.match(pattern, string)
    return bool(result)

def is_number(char):
    if '\u0030' <= char <= '\u0039':
        return True
    else:
        return False

def twoline_concat(arr_1,arr_2):
    if is_alphabet(arr_1) and is_alphabet(arr_2):
        arr_1+=' '+arr_2
    if is_chinese(arr_1) and is_chinese(arr_2):
        arr_1+=''+arr_2
    arr_2=''
    return arr_1,arr_2


if '__main__' == __name__:
    # convert txt file to array
    srt_files = []
    for file in os.listdir("./"):
        if file.endswith(".txt") or file.endswith(".srt"):
            srt_files.append(file)

    for srt_file in srt_files:
        sub_list = convert_sub_to_arr(srt_file)
        print(len(sub_list))
        i=30
        while i <len(sub_list)-1:
            
            i+=1
            if (sub_list[i-1] != '') and (sub_list[i] != ''):
                
                # two lines of EN into one line
                if is_alphabet(sub_list[i][0])  \
                    and (is_alphabet(sub_list[i-1][0]) or sub_list[i-1][0] == '-'):
                    sub_list[i-1],sub_list[i]=twoline_concat(sub_list[i-1],sub_list[i])
                
                # two lines of CN into one line
                elif is_chinese(sub_list[i][0]) \
                     and (is_chinese(sub_list[i - 1][0]) or sub_list[i-1][0] == '-'):
                    sub_list[i - 1], sub_list[i] = twoline_concat(sub_list[i - 1], sub_list[i])
                
                # if the subtitle only have En but no CN, concat this line into the last subtitle.
                elif is_timeline(sub_list[i-1]) and len(sub_list[i])>3 and is_alphabet(sub_list[i][-3]):
                    sub_list[i - 1]=''
                    sub_list[i - 2] = ''
                    sub_list[i - 4], sub_list[i] = twoline_concat(sub_list[i - 4], sub_list[i])
            # if the the first line of subtitle is empty, but the 2nd is EN
            elif is_timeline(sub_list[i-2]) and sub_list[i-1]==''\
                and len(sub_list[i])>3 and is_alphabet(sub_list[i][-3]):
                    sub_list[i - 2]=''
                    sub_list[i - 3] = ''
                    sub_list[i - 5], sub_list[i] = twoline_concat(sub_list[i - 5], sub_list[i])
            else:
                continue
            
        new_sub = []
        for inx, val in enumerate(sub_list):
                new_sub.append(val)
        out = '\n'.join(new_sub)

        with open('1_Adjusted_' + srt_file, 'w') as file:
            file.write(out)
