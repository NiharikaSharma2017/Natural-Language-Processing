import math

test = ["he somehow made this analogy sound exciting instead of hopeless", "no living humans had skeletal features remotely like these", "frequent internet and social media users do not have higher stress levels", "the sand the two women were sweeping into their dustpans was transferred into plastic bags"]

fd = open("sample.txt",'r')

def get_chars_list(str):
    chars = []
    for line in str:
       for c in line:
           if c.isalpha() or c.isspace():
            chars.append(c.lower())
    return chars


def get_trigrams_list(input_list):
   split_list = zip(*[input_list[i:] for i in range(3)])
   l1 = list(split_list)
   l2 = [''.join(each) for each in l1]
   l3 = [x for x in l2 if "\n" not in x]
   return l3


def get_trigram_context_counts(l):
    counts ={}
    context_counts = {}
    for my_trigram in l:
        if my_trigram in counts:
            counts[my_trigram] += 1
        else:
            counts[my_trigram] = 1
        my_words = list(my_trigram)
        my_words.pop()
        my_context = "".join(my_words)
        if my_context in context_counts:
            context_counts[my_context] += 1
        else:
            context_counts[my_context] = 1
    return counts, context_counts


def get_trigram_probabilities(counts, context_counts):
    probabilities = {}
    for my_trigram in counts:
        V = len(counts)
        my_words = list(my_trigram)
        my_words.pop()
        my_context = "".join(my_words)
        probabilities[my_trigram] = (counts[my_trigram] + 0.1) / (context_counts[my_context] + (0.1 * V))
    return probabilities

def get_test_data_probs(trigramlist, trained_data_probs_dict, ind):
    H = 0
    W = 0
    test_data_probs_dict = {}
    term_prob = 0
    for trigram in trigramlist:
        if trigram in trained_data_probs_dict:
            term_prob += math.log(trained_data_probs_dict[trigram], 2)
        test_data_probs_dict[trigram] = term_prob
        H += -term_prob
        W += 1
    print("Cross Entropy for Passage  {} = ".format(str(ind)) + str(H/W))
    return test_data_probs_dict



clist = get_chars_list(fd)
tlist = get_trigrams_list(clist)
count_dict, contextcount_dict = get_trigram_context_counts(tlist)
trigram_prob_dict = get_trigram_probabilities(count_dict, contextcount_dict)

test_clist1 = get_chars_list(test[0])
test_tlist1 = get_trigrams_list(test_clist1)

test_clist2 = get_chars_list(test[1])
test_tlist2 = get_trigrams_list(test_clist2)

test_clist3 = get_chars_list(test[2])
test_tlist3 = get_trigrams_list(test_clist3)

test_clist4 = get_chars_list(test[3])
test_tlist4 = get_trigrams_list(test_clist4)

get_test_data_probs(test_tlist1, trigram_prob_dict, 1)
get_test_data_probs(test_tlist2, trigram_prob_dict, 2)
get_test_data_probs(test_tlist3, trigram_prob_dict, 3)
get_test_data_probs(test_tlist4, trigram_prob_dict, 4)




















