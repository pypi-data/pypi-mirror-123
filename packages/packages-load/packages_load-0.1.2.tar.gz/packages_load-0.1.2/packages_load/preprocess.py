import bisect
import re
import pandas as pd
from timeit import default_timer as timer
import string
import warnings
import traceback as tb
import copy
from collections import OrderedDict
warnings.filterwarnings("ignore")

filtered_final = ['corporation', 'llc','inc', 'co', 'ltd', 'corp','group','industry','industries','', 'distribution',
                    'usa', 'uk', 'china', 'na', 'america', 'australia', 'company', 'gmbh', 'bv', 'the', 'wgq', 'performance',
                    'materials', 'technology', 'chemical', 'chemicals', 'kgaa', 'ag',
                    'international', 'limited', 'technologies', 'scientific','se','germany','deutschland','sa','france','europe','speciality',
                    'specialities','resin','resins','chemie','nederland','belgique','mon','belgium','bp','efficiency','resource'
                    'liwithed','italia','operations','nv','gb','krefeld','formula','sanv','surface','ab','chemistry', 'mexico','silicones']


def preProcessManufacturer(word):
  try:
    word = str(str(word).encode('ascii','ignore').decode())
    word = word.replace('.','')
    word = re.sub('[^a-zA-Z0-9 \n]', ' ', word)
    word = word.lower().split(' ')
    word = list(OrderedDict.fromkeys(word))
    [word.remove(y) for y in filtered_final if y in word]
    word = ''.join(word)
    # print('processed manufacturer name: ',word)
    return word
  except Exception as e:
        return str(e)


def preProcessRawmaterial(word):
  try:
    # word = re.sub(r'\\u[a-zA-Z0-9]{4}',' ',str(word).strip())
    word = str(word).encode('utf-8').decode().encode('ascii','ignore').decode()
    word = re.sub('[^a-zA-Z0-9 \n]',' ',str(word).strip())
    word = re.sub(r'\s+',' ',str(word).strip())
    word = word.split(' known')[0] if 'known' in word else word
    word = re.sub(r'\s+','',str(word).strip().lower())
    return word
  except Exception as e:
      return str(e)


def process_substring_raw(raw_string):
    try:
      # raw_string = re.sub(r'\\u[a-zA-Z0-9]{4}',' ',str(raw_string).strip())
      raw_string = str(str(raw_string).encode('ascii','ignore').decode())
      raw_string = raw_string.lower()
      pattern = re.compile('[%s]' % re.escape(string.punctuation))
      value = pattern.sub(' ', raw_string).split()
      ncharsSubstring = [len(x) for x in value]
      if 1 in ncharsSubstring:
        # we got some single character substrings
        # Let us do some more processing to see if those can be combined together
        raw_string_update = re.sub(r"[^a-zA-Z0-9\s]+", '',raw_string)
        value = raw_string_update.split()
        ncharsSubstring = [len(x) for x in value]
        # print(ncharsSubstring)
        if 1 in ncharsSubstring:
          return []#raw_string
      if len(value) == 1:
        return []
      return value
    except Exception as e:
      return []  #raw_string


def process_substring_manu(raw_string):
    try:
      # raw_string = re.sub(r'\\u[a-zA-Z0-9]{4}',' ',str(raw_string).strip())
      raw_string = str(str(raw_string).encode('ascii','ignore').decode())
      raw_string = raw_string.lower()
      raw_string = raw_string.replace('.','')
      raw_string = re.sub('[^a-zA-Z0-9 \n]',' ',raw_string)
      raw_string_orig = raw_string
      word = raw_string.lower().split(' ')
      word = list(OrderedDict.fromkeys(word))
      [word.remove(y) for y in filtered_final if y in word]
      raw_string = ' '.join(word)
      pattern = re.compile('[%s]' % re.escape(string.punctuation))
      value = pattern.sub(' ', raw_string).split()
      ncharsSubstring = [len(x) for x in value]
      if 1 in ncharsSubstring:
        # # we got some single character substrings
        # # Let us do some more processing to see if those can be combined together
        # raw_string_update = re.sub(r"[^a-zA-Z0-9\s]+", '',raw_string)
        # value = raw_string_update.split()
        # ncharsSubstring = [len(x) for x in value]
        # # print(ncharsSubstringd)
        # if 1 in ncharsSubstring:
          return raw_string
      return value
    except Exception as e:
      return []#raw_string
