def isreapeated(dic):
    for key, value in dic.items():
       if value > 1:
           return True;
    return False;


def clean_keywords(text):
    keywords = text.split(";")
    word_count = {}
    lista_repetidas=[]
    unique_keywords = []
    for keyword in keywords:
        words = keyword.split()
        for word in words:
           if word in word_count:
               word_count[word] += 1
           else:
               word_count[word] = 1

    if isreapeated(word_count):
        for key, value in word_count.items():
           if value > 1:
               repetidas=[]
               for keyword in keywords:
                   wordss=keyword.split()
                   if key in wordss:
                       repetidas.append(keyword)
               lista_repetidas.append(repetidas)

        for keyword in keywords:
            words = keyword.split()
            if any(word_count[word] > 1 for word in words):
                continue
            else:
                unique_keywords.append(keyword)

        for lista in lista_repetidas:
            unique_keywords.append(lista[0])
            unique_keywords.append(lista[1])
        unique_phrases = set()
        for keyword in unique_keywords:
            words = tuple(sorted(keyword.split()))
            unique_phrases.add(words)
        result = [" ".join(words) for words in unique_phrases]
        keywords_string=';'.join(result)
        return keywords_string
    else:
        return text
text="education technology;learning technology;education tools;innovations edtech;access educational;literacy software;education experimental;edtech innovations;education;technologyaided instruction"
print(clean_keywords(text))
    