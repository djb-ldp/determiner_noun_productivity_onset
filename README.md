# LDP Onset of Determiner Noun Productivity

This repo contains code for the forthcoming paper from ....
The repo directory is structured as 


## Requirements

python version 3.6 or above

Outside of the standard python3 library the additional dependencies are: pandas, numpy, spacy
 

```bash

```

## Examples CLI

```bash
>>>from extract_determiner_noun_phrases import SimpleDeterminerNounConstruction
>>>sdnc = SimpleDeterminerNounConstruction()
>>>sdnc.det_noun_phrase('I want to get your book on the table') 
{'det_noun_phrase_type': 'def_np', 'det_token': 'the', 'noun_token': 'table', 'noun_phrase': 'the table', 'det_noun_dist': 0, 'alt_det_tokens': ['your', 'the'], 'alt_noun_tokens': '', 'alt_noun_phrases': ['your book', 'the table'], 'alt_det_noun_dists': [0, 0], 'alt_noun_phrase_types': ['poss_np', 'def_np']}


```

## Multiple Utterances: use list comprehension, and dict .get() method to pass dict keys

```bash
>>>li = ['I want to get your book on the table', 'Look at the red ball!', '']
>>>[sdnc.det_noun_phrase(x).get('det_noun_phrase_type') for x in li]
['def_np', 'def_np', None]
>>>[sdnc.det_noun_phrase(x).get('alt_noun_phrase_types') for x in li]
[['poss_np', 'def_np'], [], None]
>>>[sdnc.det_noun_phrase(x).get('noun_phrase') for x in li]
['the table', 'the ball', None]
>>>[sdnc.det_noun_phrase(x).get('alt_noun_phrases') for x in li]
[['your book', 'the table'], '', None]

```

## License
[MIT](https://choosealicense.com/licenses/mit/)
