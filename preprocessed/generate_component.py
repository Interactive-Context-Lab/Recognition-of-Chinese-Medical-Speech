'''
To generate the file that preprocessing progress needed.
'''

import os
import json

train_manifest = "/media/ee303/My_Passport/Joint/new_exp/dataA/train_manifest.csv"
output_path = "/media/ee303/My_Passport/Joint/new_exp/dataA/preprocess"


def sep_seq(seq):
    """
    return a list of sentence
    e.g. "Ada{asd}qe{qs}a" -> [A,s,a,{asd},q,e,{qs},a]

    :param seq: input sentence
    :return: list of sentence
    """
    temp = []
    is_eng_word = False
    word_temp = ""
    for c in seq:
        word_temp = word_temp + c
        if c == "{" or c == "}" or c == "<" or c == ">":
            is_eng_word = not is_eng_word
            if not is_eng_word:
                temp.append(word_temp)
                word_temp = ""
        elif not is_eng_word:
            temp.append(word_temp)
            word_temp = ""
    return temp


with open(train_manifest, "r") as f:
    train_files = f.readlines()
train_files = [a.strip() for a in train_files]

label_kinds = []
for i in train_files:
    with open(i.split(",")[-1], "r") as f:
        label = f.readlines()[0].strip()
    for j in sep_seq(label):
        if j not in label_kinds:
            label_kinds.append(j)

label_kinds.sort()
with open(os.path.join(output_path, "label.json"), "w") as f:
    f.write('["_", ')
    for j in label_kinds:
        f.write('"{}", '.format(j))
    f.write('"{<unk>}", " "]')


eng_syllable = []
other_words = []
for i in train_files:
    label = i.split(",")[1]
    with open(label, "r") as f:
        content = f.readlines()[0].strip()
    for j in sep_seq(content):
        if len(j) > 1:
            eng_syllable.append(j)
        else:
            other_words.append(j)

# English to word and word to English file
E2C_dic = {}
count = 19968
for i in eng_syllable:
    while i not in E2C_dic:
        if chr(count) in other_words:
            count = count + 1
        else:
            E2C_dic[i] = chr(count)
            count = count + 1
while 1:
    if chr(count) in other_words:
        count = count + 1
    else:
        E2C_dic['{<unk>}'] = chr(count)
        break

with open(os.path.join(output_path,'E2C.json'), 'w') as outfile:
    json.dump(E2C_dic, outfile,ensure_ascii=False)
    outfile.write('\n')

C2E_dic = {}
for i in E2C_dic.keys():
    C2E_dic[E2C_dic[i]] = i
with open(os.path.join(output_path,'C2E.json'), 'w') as outfile:
    json.dump(C2E_dic, outfile,ensure_ascii=False)
    outfile.write('\n')