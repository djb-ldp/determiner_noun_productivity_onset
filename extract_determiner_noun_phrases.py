def det_nps_extraction(utt):
    
        
    """
    
    Simple function that extracts determiner noun phrases from utterances and or text data
    Uses SpaCy3 to assign part-of-speech tags and lemmatize data; spacy loaded and initiated as nlp
    Includes and counts determiner noun phrases with intervening adjectives
    Initiate class and then call method on text data
    
    PARAMETERS x: str
    
    RETURNS
    
    list
    
    
    values:
    
    determiner noun phrase type -> str: indefinite noun phrase, definite noun phrase, 
    demonstrative noun phrase, possessive noun phrase, str: determiner token, str: lemmatized noun token, 
    str: concatenated noun phrase determiner + lemmatized token, int: determiner distance from noun; 
    if the utterance or string contains multiple determiner noun phrases the will include non-empty list. 
    The alternative (secondary, terietary, etc.) determiner noun phrases, alternative determiner noun tokens, alternative lemmatized nouns, alternative
    determiner noun phrases, alternative determiner noun distance of number words between determiner and noun;
    otherwise the output is an empty list.
    
    
    
    
    """

    utt = utt.strip().lower()
    
    utt_li = utt.split()
    
    utt_di = {i:x for i, x in enumerate(utt_li)}
    
    det_di = {'all_dets': ['a', 'an', 'the'],

                      'indef_dets': ['a', 'an'],

                      'def_dets': ['the'],

                      'poss_dets':  ['my', 'mine', 'your', 'yours', 'their', 'theirs', 
                      'his', 'her', 'hers', 
                      'its', 'ours', 'our'],

                      'demo_dets': ['this', 'that', 'these', 'those']


            }
    
    
    utt_nlp = nlp(utt)
    
    pos_li = [x.pos_ for x in utt_nlp]
    
    utt_det_intersect_len = len(set(utt.strip().lower().split()).intersection(set(det_di['all_dets'])))
    
    utt_det_set = set(utt.strip().lower().split()).intersection(set(det_di['all_dets']))



            ## check to ensure that there is at least one or more determiner in the text set,
            ## otherwise return empty dictionry {}
    nps = []
    if utt_det_intersect_len >= 1:
        for det in utt_det_set:
            for i, x in enumerate(utt_li):
                if x == det:
                    det_ix = i
                    while i < len(utt_li):
                        if pos_li[i] == 'NOUN' or pos_li[i] == 'NUM' or pos_li[i] == 'PROPN':
                            if (i+1 < len(utt_li)) and (pos_li[i+1] == 'NOUN'):
                                nps.append(' '.join(utt_li[det_ix:i+2]))
                                break
                            else:
                                nps.append(' '.join(utt_li[det_ix:i+1]))
                                break

                        else:
                            i+=1
                            
                                
                                
        return nps
                                
                            
                                
                            
        
        
        
    else:
        
        return []

    
        
        
def find_the(utt):
    
    utt_li = utt.strip().lower().split()
    
    if 'the' in utt_li:
        return 1
    else:
        return 0
    

    
def find_a(utt):
    
    utt_li = utt.strip().lower().split()
    
    if ('a' in utt_li) or ('an' in utt_li):
        return 1
    else:
        return 0
    
    

    
def find_a_the(utt):
    
    utt_li = utt.strip().lower().split()
    
    if ('a' in utt_li) or ('an' in utt_li) or ('the' in utt_li):
        return 1
    else:
        return 0
    
    
def return_two_word_nps(utt_li):
    nli = []
    for utt in utt_li:
        try:
        
            nli.append(utt.split()[0] + ' ' + utt.split()[-1])
        
        except:
            nli.append(utt)
            
        
    return nli


def lemma_noun(utt_list):
    nps_lemma_li = []
    for utt in utt_list:
        lemma_utt = ' '.join([x.lemma_ for x in nlp(utt)])
        nps_lemma_li.append(lemma_utt)
        
    return nps_lemma_li
    
    
        
def org_yang_analysis_1_2(pdf, child_parent):

    result = []


    pdf = [x for x in pdf if (len(x.split()) == 2) and (x.split()[0] == 'a' or x.split()[0] == 'the')]


    def Harmonic(n):
        s=0
        for i in range(1, n+1):
            s+=1.0/i
        return s

    def expected_overlap(N, S, r, b):
        hN = Harmonic(N)
        p = 1.0/(r*hN)
        eo = 1 - sum( [ math.pow((p*di+1.0-p), S) for di in [b, 1.0-b] ] ) + math.pow(1-p, S)
        assert eo>=-1, '%d, %.6f'%(r, eo)
        return eo

    def average_expected_overlap(N, S, b):
        sumo = 0
        for r in range(1, N+1):
            sumo += expected_overlap(N, S, r, b)
        return sumo/N

    def freqcounts(word, data):
        ccc = 0
        for i in range(0, len(data)):
            if word == data[i].split()[1]:
                ccc += 1
        return ccc

    def uniqwords(data):
        ccc = 0
        uniqw = []
        for i in range(0, len(data)):
            nnn = data[i].split()[1]
            if nnn not in uniqw:
                uniqw.append(nnn)
                ccc += 1
        return ccc

    def calculate_overlap(data): # returns s, n, and empirical overlap
        result = []
        result.append(len(data))

        uniqnoun = []
        for i in range(0, len(data)):
            nnn = data[i].split()[1]
            if nnn not in uniqnoun:
                uniqnoun.append(nnn)
        result.append(len(uniqnoun))

        both = 0 # counts of nouns that have overlap
        for i in range(0, len(uniqnoun)):
            a = 0
            the = 0
            for j in range(0, len(data)):
                if uniqnoun[i] == data[j].split()[1]:
                    if data[j].split()[0] == 'a':
                        a = 1
                    if data[j].split()[0] == 'the':
                        the = 1
            if a == 1 and the == 1:
                both += 1

        result.append(both)

        return result

    def find_bias(data):

        uniqw = []
        for i in range(0, len(data)):
            nnn = data[i].split()[1]
            if nnn not in uniqw:
                uniqw.append(nnn)


        big = 0
        small = 0
        for i in range(0, len(uniqw)):
            a = 0
            the = 0
            for j in range(0, len(data)):
                if uniqw[i] == data[j].split()[1]:
                    if data[j].split()[0] == 'a':
                        a += 1
                    else:
                        the +=1
            if a >= the:
                big += a
                small += the
            else:
                big += the
                small += a
        return float(big)/float(big+small)
    
    p_tmp = calculate_overlap(pdf)
    p_S = int(p_tmp[0])
    p_N = int(p_tmp[1])
    p_O = int(p_tmp[2])
    p_bias = find_bias(pdf)
    
    



    
    
    return [child_parent, p_N, p_S, p_bias, (float(p_S)/float(p_N)), (float(p_O)/float(p_N)), average_expected_overlap(p_N, p_S, p_bias)]
        

def prod_det_nps(det_df_all_nouns_li):

    nps_set_di = {}
    for x in set(det_df_all_nouns_li):
        if x.split()[1] not in nps_set_di.keys():
            nps_set_di[x.split()[1]] = {'dets_li': []}

            nps_set_di[x.split()[1]]['dets_li'].append(x.split()[0])

        else:

            nps_set_di[x.split()[1]]['dets_li'].append(x.split()[0])

    prod_nouns = [k for k, v in nps_set_di.items() if len(nps_set_di[k]['dets_li']) >=2]

    if len(prod_nouns) >= 1:



        return {'productive_bool': 1, 'num_productive_nouns': len(prod_nouns)}

    else:
        return {'productive_bool': 0, 'num_productive_nouns': len(prod_nouns)}

def remove_duplicate_stutter_dets(utt_list):
    new_utt_list = []
    for utt in utt_list:
        utt = utt.strip().lower()
        utt_li = utt.split()
        utt_word_counts_di = dict(Counter(utt_li))

        utt_a_counts = 0
        utt_the_counts = 0

        if (utt_word_counts_di.get('a') is not None):
            utt_a_counts = utt_word_counts_di.get('a')


        if (utt_word_counts_di.get('the') is not None):
            utt_the_counts = utt_word_counts_di.get('the')


        if (utt_a_counts > 1 ) or (utt_the_counts > 1) or (utt_a_counts + utt_the_counts > 1):
            new_utt_list.append('')

        else:

            new_utt_list.append(utt)
            
    return new_utt_list

def filter_letters(utt_list):
    new_utt_list = []
    for utt in utt_list:
        new_utt = []
        utt = utt.strip().lower()
        for x in utt.split():
            if x == 'l':
                pass
            else:
                new_utt.append(x)
        new_utt = ' '.join(new_utt)
        new_utt_list.append(new_utt)
        
    return new_utt_list
                

def remove_punctuation(input_string: str) -> str:
    """
    This function removes all punctuation from the input string.
    """
    return input_string.translate(str.maketrans('', '', string.punctuation))

def remove_punctuation_and_apostrophe(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\s]+|'s", "", s)


def extract_noun_phrases(input_string: str) -> list:
    """
    This function extracts all noun phrases from the input string.
    """
    # Load the spaCy model
    nlp = spacy.load('en_core_web_lg')
    
    # Parse the input string
    doc = nlp(input_string)
    
    # Extract the noun phrases
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    
    return noun_phrases

    
    

def one_det_nps_extraction(utt):

    utt = utt.strip().lower()
    
    utt_li = utt.split()
    
    utt_di = {i:x for i, x in enumerate(utt_li)}
    
    det_di = {'all_dets': ['a', 'an', 'the'],

                      'indef_dets': ['a', 'an'],

                      'def_dets': ['the'],

                      'poss_dets':  ['my', 'mine', 'your', 'yours', 'their', 'theirs', 
                      'his', 'her', 'hers', 
                      'its', 'ours', 'our'],

                      'demo_dets': ['this', 'that', 'these', 'those']


            }
    
    
    utt_nlp = nlp(utt)
    
    pos_li = [x.pos_ for x in utt_nlp]

    
    utt_det_intersect_len = len(set(utt.strip().lower().split()).intersection(set(det_di['all_dets'])))
    
    utt_det_set = set(utt.strip().lower().split()).intersection(set(det_di['all_dets']))



            ## check to ensure that there is at least one or more determiner in the text set,
            ## otherwise return empty dictionry {}
    nps = []
    utt_det_count = 0
    if utt_det_intersect_len >= 1:
        for det in utt_det_set:
            
            if utt_det_count < 1:
                utt_det_count +=1
                for i, x in enumerate(utt_li):
                    if x == det:
                        det_ix = i
                        while i < len(utt_li):
                            if pos_li[i] == 'NOUN' or pos_li[i] == 'NUM':
                                if (i+1 < len(utt_li)) and (pos_li[i+1] == 'NOUN'):
                                    nps.append(' '.join(utt_li[det_ix:i+2]))

                                    break
                                else:
                                    nps.append(' '.join(utt_li[det_ix:i+1]))
                                    break

                            else:
                                i+=1
                


                                
        return nps
                                
                            
                                
                            
        
        
        
    else:
        
        return []
    

    

    
    

    
    
def prod_det_nps(det_df_all_nouns_li):

    nps_set_di = {}
    for x in set(det_df_all_nouns_li):
        if x.split()[1] not in nps_set_di.keys():
            nps_set_di[x.split()[1]] = {'dets_li': []}

            nps_set_di[x.split()[1]]['dets_li'].append(x.split()[0])

        else:

            nps_set_di[x.split()[1]]['dets_li'].append(x.split()[0])

    prod_nouns = [k for k, v in nps_set_di.items() if len(nps_set_di[k]['dets_li']) >=2]

    if len(prod_nouns) >= 2:



        return {'productive_bool': 1, 'num_productive_nouns': len(prod_nouns), 'prod_nouns': prod_nouns}

    else:
        return {'productive_bool': 0, 'num_productive_nouns': len(prod_nouns), 'prod_nouns': prod_nouns}

def find_def_dets(x):
    
    if len(x.split()) == 2:
        if ((x.split()[0] == 'the') or (x.split()[0] == 'a')):
            return "det_det_nps"
        
        else:
            return ""
    else:
        return ""

def find_bias(data):

    uniqw = []
    for i in range(0, len(data)):
        nnn = data[i].split()[1]
        if nnn not in uniqw:
            uniqw.append(nnn)


    big = 0
    small = 0
    for i in range(0, len(uniqw)):
        a = 0
        the = 0
        for j in range(0, len(data)):
            if uniqw[i] == data[j].split()[1]:
                if data[j].split()[0] == 'a':
                    a += 1
                else:
                    the +=1
        if a >= the:
            big += a
            small += the
        else:
            big += the
            small += a
    return float(big)/float(big+small)


def find_bias_per_noun(data):
    
    bias_di = {}

    uniqw = []
    for i in range(0, len(data)):
        nnn = data[i].split()[1]
        if nnn not in uniqw:
            uniqw.append(nnn)
            bias_di[nnn] = 0


    big = 0
    small = 0
    for i in range(0, len(uniqw)):
        a = 0
        the = 0
        for j in range(0, len(data)):
            if uniqw[i] == data[j].split()[1]:
                if data[j].split()[0] == 'a':
                    a += 1
                else:
                    the +=1
        if a >= the:
            big += a
            small += the
            bias_di[uniqw[i]] = float(big)/float(big+small)

        else:
            big += the
            small += a
            bias_di[uniqw[i]] = float(big)/float(big+small)
    
    return bias_di

def find_repeated_nouns(noun_phrases):
    noun_counts = {}
    result_nouns = set()

    for phrase in noun_phrases:
        words = phrase.split()
        determiner = words[0].lower()
        noun = words[1].lower()

        if determiner in ['a', 'the']:
            key = determiner + ' ' + noun
            noun_counts[key] = noun_counts.get(key, 0) + 1

            if noun_counts[key] == 2:
                result_nouns.add(noun)

    return list(result_nouns)

# Example usage:
noun_phrases = ["a cat", "the dog", "a cat", "the bird", "a dog"]
result = find_repeated_nouns(noun_phrases)
print(result)


extract_noun_phrases('and a other baby one.')

    
det_nps_extraction(re.sub(' +', ' ',(remove_punctuation("### this is the bed -- for the Barbie doll."))).strip())
