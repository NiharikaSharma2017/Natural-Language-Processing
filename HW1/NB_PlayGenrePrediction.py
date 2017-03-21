import argparse, glob, os, re, operator, math, sys

__author__ = 'Niharika Sharma'

def get_all_files_in_dir(dir_path):
    filepath_list = []
    for filepath in glob.glob(os.path.join(dir_path, '*.txt')):
        filepath_list.append(filepath)
    return filepath_list


def assign_files(filelist, f):
    Selected = None
    for i in range(len(filelist)):
        training_list = []
        Selected = filelist[i]
        for file in filelist:
            if file == Selected:
                pass
            else:
                training_list.append(file)
        process_training_and_test_data(Selected, training_list, f)


def process_training_and_test_data(testfile, training_file_list,f):
    comedies = []
    tragedies = []
    true_genre = ""
    predicted_genre = ""
    if "comedies" in testfile:
        true_genre = "Comedy"
    else:
        true_genre = "Tragedy"
    for fpath in training_file_list:
        if "comedies" in fpath:
            comedies.append(fpath)
        else:
            tragedies.append(fpath)
    Comedies_word_wordcount_dict, Comedies_word_doccount_dict = read_training_files(comedies)
    Tragedies_word_wordcount_dict, Tragedies_word_doccount_dict = read_training_files(tragedies)
    Comedies_word_wordcount_dict = compare_dicts_fill_gaps(Tragedies_word_wordcount_dict, Comedies_word_wordcount_dict)
    Tragedies_word_wordcount_dict = compare_dicts_fill_gaps(Comedies_word_wordcount_dict, Tragedies_word_wordcount_dict)
    Comedies_word_doccount_dict = compare_dicts_fill_gaps(Tragedies_word_doccount_dict, Comedies_word_doccount_dict)
    Tragedies_word_doccount_dict = compare_dicts_fill_gaps(Comedies_word_doccount_dict, Tragedies_word_doccount_dict)
    Comedies_word_wordcount_dict, Tragedies_word_wordcount_dict = remove_unwanted_words(Comedies_word_wordcount_dict, Comedies_word_doccount_dict, Tragedies_word_wordcount_dict, Tragedies_word_doccount_dict)
    Comedies_Prob = calculate_probabilities(Comedies_word_wordcount_dict)
    Tragedies_Prob = calculate_probabilities(Tragedies_word_wordcount_dict)
    testfile_com_prob = calculate_com_tra_prob(testfile, Comedies_Prob)
    testfile_tra_prob = calculate_com_tra_prob(testfile, Tragedies_Prob)
    ratio = testfile_com_prob/testfile_tra_prob
    if testfile_com_prob <= testfile_tra_prob:
        predicted_genre = "Tragedy"
    else:
        predicted_genre = "Comedy"
    fname = testfile.split("/")[-1:][0]
    filestr = fname + '\t\t\t' +true_genre+ '\t\t\t' +predicted_genre+ '\t\t\t' +str(ratio) + '\n'
    f.write(filestr)


def calculate_com_tra_prob(testfile, prob_dict):
    test_file_word_list = read_test_file(testfile)
    term_prob = 0
    for term in test_file_word_list:
        if term in prob_dict:
            term_prob += math.log(prob_dict[term])
    return term_prob


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


def read_test_file(filename):
    words_list = []
    with open(filename) as f:
        text = ''.join(f.readlines())
        words = text.split()
        lwords = [w.strip().lower() for w in words]
        for raw_term in lwords:
            term = re.sub("[^a-zA-Z]+", "", raw_term)
            words_list.append(term)
    return words_list


def main():
    args = sys.argv
    path_to_comedies = args[1]
    path_to_tragedies = args[2]
    Comedies = get_all_files_in_dir(path_to_comedies)
    Tragedies = get_all_files_in_dir(path_to_tragedies)
    All_plays = Comedies + Tragedies
    f = open('PlayGenrePredictionOutputFile', 'w')
    f.write("Play Name"+ '\t\t' +"True Genre"+ '\t\t' +"Predicted Genre"+ '\t\t' +"Log Likelihood - Comedy/Tragedy" + '\n')
    assign_files(All_plays, f)
    f.close()


if __name__ == "__main__":
    main()