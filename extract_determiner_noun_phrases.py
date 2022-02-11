class SimpleDeterminerNounConstruction():
    
    """
    
    Simple class with one function that extracts determiner noun phrases from utterances and or text data
    Uses SpaCy3 to assign part-of-speech tags and lemmatize data; spacy loaded and initiated as nlp
    Includes and counts determiner noun phrases with intervening adjectives
    Initiate class and then call method on text data
    
    PARAMETERS x: str
    
    RETURNS
    
    dictionary
    
    keys:
    
    'det_noun_phrase_type'
    'det_token'
    'noun_token'
    'noun_phrase'
    'det_noun_dist'
    'alt_det_tokens'
    'alt_noun_tokens'
    'alt_noun_phrases'
    'alt_det_noun_dists'
    'alt_noun_phrase_types'
    
    
    values:
    
    determiner noun phrase type -> str: indefinite noun phrase, definite noun phrase, 
    demonstrative noun phrase, possessive noun phrase, str: determiner token, str: lemmatized noun token, 
    str: concatenated noun phrase determiner + lemmatized token, int: determiner distance from noun; 
    if the utterance or string contains multiple determiner noun phrases the dictioanry will include keys with non-empty lists as values. 
    The alternative determiner noun phrases, alternative determiner noun tokens, alternative lemmatized nouns, alternative
    determiner noun phrases, alternative determiner noun distance of number words between determiner and noun;
    otherwise the output is an empty dictionary
    
    
    EXAMPLE:
    
    sndc = SimpleDeterminerNounConstruction()
    sndc.det_noun_phrase("my car is bigger than your car")
    
    OUTPUT:
    
    
    
    {'det_noun_phrase_type': 'poss_np',
     'det_token': 'your',
     'noun_token': 'car',
     'noun_phrase': 'your car',
     'det_noun_dist': 0,
     'alt_det_tokens': ['my', 'your'],
     'alt_noun_tokens': '',
     'alt_noun_phrases': ['my car', 'your car'],
     'alt_det_noun_dists': [0, 0],
     'alt_noun_phrase_types': ['poss_np', 'poss_np']}
    
    
    """
    
   
    def det_noun_phrase(self, x):
        
        # import fucntion dependencies 
        
        from collections import Counter
        
        di = {} # initiate empty dictionary
        
        nps = ['NOUN', 'PROPN', 'PRON'] # spacy pos tag types for nouns 
        
        # determiner dictionary of all determiners, definites, indefinites, possessives, demonstratives 
        
        det_di = {'all_dets': ['a', 'an', 'the',
                 'my', 'mine', 'your', 'yours', 'their', 'theirs', 
                  'his', 'her', 'hers', 
                  'its', 'ours', 'our',
                  'this', 'that', 'these', 'those'],
                  
                  'indef_dets': ['a', 'an'],
                  
                  'def_dets': ['the'],
                  
                  'poss_dets':  ['my', 'mine', 'your', 'yours', 'their', 'theirs', 
                  'his', 'her', 'hers', 
                  'its', 'ours', 'our'],
                  
                  'demo_dets': ['this', 'that', 'these', 'those']
                  
                  
        }
        

        ## check to ensure that there is at least one or more determiner in the text set,
        ## otherwise return empty dictionry {}
        
        if len(set(x.strip().lower().split()).intersection(set(det_di['all_dets']))) >= 1:
            
        
        
        
            x = nlp(x.strip().lower()) # strip extra spaces, normalized the case, and cast str -> spacy Doc type
            

            pos_tags = [token.pos_ for token in x] # list comprehension for part of speech tags
            
            pos_deps = [token.dep_ for token in x] # list comprehension for dependencies 
            
            
            ## check if noun in pos_tags list otherwise return empty dict {}
            if 'NOUN' not in pos_tags:
                return {}
                
            ### create counts of pos tags

            pos_counts = Counter(pos_tags)

            
            ##


            if len(set(pos_tags).intersection(set(nps))) <= 0:
                return {}

            elif 'DET' in pos_counts.keys():
                if pos_counts['DET'] == 1:

                    for token in x:
                        if (token.pos_ == 'DET') and (token.dep_ != 'nsubj') and (token.text) in det_di['all_dets']:                                 
                            det_index = token.i
                            det_token = token.text
                            for w in x[token.i:]:
                                if w.pos_ in nps:
                                    noun_index = w.i
                                    noun_token = w.text

                                    det_noun_dist = (noun_index - det_index) - 1

                                    noun_phrase = det_token + ' ' + noun_token


                                    if det_token in det_di['indef_dets']:
                                        di['det_noun_phrase_type'] = 'indef_np'

                                    if det_token in det_di['def_dets']:

                                        di['det_noun_phrase_type'] = 'def_np'

                                    if det_token in det_di['poss_dets']:

                                        di['det_noun_phrase_type'] = 'poss_np'

                                    if det_token in det_di['demo_dets']:
                                        di['det_noun_phrase_type'] = 'demo_np'




                                    di['det_token'] = det_token
                                    di['noun_token'] = noun_token
                                    di['noun_phrase'] = noun_phrase
                                    di['det_noun_dist'] =  det_noun_dist

                                    di['alt_det_tokens'] = ''
                                    di['alt_noun_tokens'] = ''
                                    di['alt_noun_phrases'] = ''
                                    di['alt_det_noun_dists'] = np.nan
                                    di['alt_noun_phrase_types'] = []

                                    return di


                else:

                    det_index_li = []
                    det_token_li = []
                    noun_index_li = []
                    noun_token_li = []
                    det_noun_dist_li = []
                    det_noun_phrases_li = []
                    alt_noun_phrase_types_li = []

                    for token in x:

                        if (token.pos_ == 'DET') and (token.dep_ != 'nsubj') and (token.text) in det_di['all_dets']:  
                            det_index = token.i
                            det_token = token.text
                            det_index_li.append(token.i)
                            det_token_li.append(token.text)
                            for w in x[token.i:]:
                                if w.pos_ in nps:
                                    noun_index = w.i
                                    noun_token = w.text

                                    noun_index_li.append(w.i)

                                    noun_token_li.append(w.text)

                                    det_noun_dist = (noun_index - det_index) - 1

                                    noun_phrase = det_token + ' ' + noun_token



                    if len(noun_index_li) == 0:
                        try:
                            for token in x:
                                if token.pos_ in nps:
                                    noun_index = token.i
                                    noun_token = token.text

                                    noun_index_li.append(token.i)

                                    noun_token_li.append(token.text)

                                    det_noun_dist = (noun_index - det_index)

                                    noun_phrase = det_token + ' ' + noun_token
                        except:
                            return {}
                            


                    for i in range(len(det_index_li)):


                        try:

                            det_noun_dist_li.append((noun_index_li[i] - det_index_li[i]) - 1)
                            det_noun_phrases_li.append(det_token_li[i] + ' ' + noun_token_li[i])

                        except:

                            det_noun_dist_li.append((noun_index_li[0] - det_index_li[i]) - 1)
                            det_noun_phrases_li.append(det_token_li[i] + ' ' + noun_token_li[0])



                        if det_token_li[i] in det_di['indef_dets']:
                            alt_noun_phrase_types_li.append('indef_np')

                        if det_token_li[i] in det_di['def_dets']:
                            alt_noun_phrase_types_li.append('def_np')

                        if det_token_li[i] in det_di['poss_dets']:
                            alt_noun_phrase_types_li.append('poss_np')

                        if det_token_li[i] in det_di['demo_dets']:
                            alt_noun_phrase_types_li.append('demo_np')


                    if det_token in det_di['indef_dets']:
                        di['det_noun_phrase_type'] = 'indef_np'

                    if det_token in det_di['def_dets']:

                        di['det_noun_phrase_type'] = 'def_np'

                    if det_token in det_di['poss_dets']:

                        di['det_noun_phrase_type'] = 'poss_np'

                    if det_token in det_di['demo_dets']:
 
                        di['det_noun_phrase_type'] = 'demo_np'


                    di['det_token'] = det_token
                    di['noun_token'] = noun_token
                    di['noun_phrase'] = noun_phrase
                    di['det_noun_dist'] =  det_noun_dist

                    di['alt_det_tokens'] = det_token_li
                    di['alt_noun_tokens'] = ''
                    di['alt_noun_phrases'] = det_noun_phrases_li
                    di['alt_det_noun_dists'] = det_noun_dist_li
                    di['alt_noun_phrase_types'] = alt_noun_phrase_types_li


                    return di



            else:

                return {}
        else:

            return {}
        
            
            
