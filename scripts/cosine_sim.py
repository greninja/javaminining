import re, math
from collections import Counter

WORD = re.compile(r'\w+')

def text_to_vector(text):
	
     words = WORD.findall(text)
     return Counter(words)

def get_cosine(str1, str2):

    vector1 = text_to_vector(str1)
    vector2 = text_to_vector(str2)
    intersection = set(vector1.keys()) & set(vector2.keys())
    numerator = sum([vector1[x] * vector2[x] for x in intersection])

    sum1 = sum([vector1[x]**2 for x in vector1.keys()])
    sum2 = sum([vector2[x]**2 for x in vector2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator