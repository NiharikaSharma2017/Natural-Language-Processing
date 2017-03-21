import argparse, glob, os, re, operator, math, sys

__author__ = 'Niharika Sharma'


def get_all_files_in_dir(dir_path):
    filepath_list = []
    for filepath in glob.glob(os.path.join(dir_path, '*.txt')):
        filepath_list.append(filepath)
    return filepath_list


def read_training_files(flist):
    words_list = []
    word_wordcount_dict = {}
    word_doccount_dict = {}
    for filename in flist:
        wset=set()
        with open(filename) as f:
            text = ''.join(f.readlines())
            words=text.split()
            lwords = [w.strip().lower() for w in words]
            for raw_term in lwords:
                term = re.sub("[^a-zA-Z]+", "", raw_term)
                words_list.append(term)
                wset.add(term)
            for each in wset:
                if each not in word_doccount_dict:
                    word_doccount_dict[each] = 1
                else:
                    word_doccount_dict[each] += 1
    for w in words_list:
        if w not in word_wordcount_dict:
            word_wordcount_dict[w] = 1
        else:
            word_wordcount_dict[w] += 1
    return(word_wordcount_dict, word_doccount_dict)


def compare_dicts_fill_gaps(d1, d2):
    for key,value in d1.items():
        if key not in d2:
            d2[key] = 0
    return d2


def remove_unwanted_words(com_wc, com_dc, tra_wc, tra_dc):
    term_count_less_than_5_wordlist = []
    for key in list(com_wc):
        if tra_wc[key] + com_wc[key] < 5:
            term_count_less_than_5_wordlist.append(key)
    for each in term_count_less_than_5_wordlist:
        if com_dc[each] < 2:
            del com_wc[each]
            del tra_wc[each]
        if tra_dc[each] < 2:
            try:
                del tra_wc[each]
                del com_wc[each]
            except KeyError:
                pass
    return com_wc, tra_wc

def calculate_probabilities(dic):
    prob_dic = {}
    V = len(dic)
    count = sum(dic.values())
    for k, v in dic.items():
        prob = (float(v) + 0.1) / (count + (0.1*V))
        prob_dic[k] = prob
    return prob_dic


def calculate_top_20(com_prob, tra_prob):
    com_to_tra_log_ratio = {}
    tra_to_com_log_ratio = {}
    for key in com_prob.keys():
        com_to_tra_log_ratio[key] = math.log(com_prob[key]) - math.log(tra_prob[key])
        tra_to_com_log_ratio[key] = math.log(tra_prob[key]) - math.log(com_prob[key])
    top_20_com_to_tra_log_ratio = sorted(com_to_tra_log_ratio.items(), key=operator.itemgetter(1), reverse=True)[:20]
    top_20_tra_to_com_log_ratio = sorted(tra_to_com_log_ratio.items(), key=operator.itemgetter(1), reverse=True)[:20]
    return top_20_com_to_tra_log_ratio, top_20_tra_to_com_log_ratio



def main():
    args = sys.argv
    path_to_comedies = args[1]
    path_to_tragedies = args[2]
    Comedies = get_all_files_in_dir(path_to_comedies)
    Tragedies = get_all_files_in_dir(path_to_tragedies)
    Comedies_word_wordcount_dict, Comedies_word_doccount_dict = read_training_files(Comedies)
    Tragedies_word_wordcount_dict, Tragedies_word_doccount_dict = read_training_files(Tragedies)
    Comedies_word_wordcount_dict = compare_dicts_fill_gaps(Tragedies_word_wordcount_dict, Comedies_word_wordcount_dict)
    Tragedies_word_wordcount_dict = compare_dicts_fill_gaps(Comedies_word_wordcount_dict, Tragedies_word_wordcount_dict)
    Comedies_word_doccount_dict = compare_dicts_fill_gaps(Tragedies_word_doccount_dict, Comedies_word_doccount_dict)
    Tragedies_word_doccount_dict = compare_dicts_fill_gaps(Comedies_word_doccount_dict, Tragedies_word_doccount_dict)
    Comedies_word_wordcount_dict, Tragedies_word_wordcount_dict = remove_unwanted_words(Comedies_word_wordcount_dict, Comedies_word_doccount_dict, Tragedies_word_wordcount_dict, Tragedies_word_doccount_dict)
    Comedies_Prob = calculate_probabilities(Comedies_word_wordcount_dict)
    Tragedies_Prob = calculate_probabilities(Tragedies_word_wordcount_dict)
    comic, tragic = calculate_top_20(Comedies_Prob, Tragedies_Prob)
    f = open('Vocabulary', 'w')
    for key in Comedies_Prob.keys():
        s = key + "\n"
        f.write(s)
    f.close()
    print("Top 20 Comic Features:")
    for each in comic:
        print(each[0] + '\t' + str(each[1]))
    print('\n\n\n')
    print("Top 20 Tragic Features:")
    for each in tragic:
        print(each[0] + '\t' + str(each[1]))



if __name__ == "__main__":
    main()