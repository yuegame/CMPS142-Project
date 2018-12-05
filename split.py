def tokenize(s):
    last_punct = False
    combined = []
    words = s.split(' ')
    i = 0
    while i < len(words) - 1:
        if i != len(words) - 1:
            if(not words[i+1][0].isalpha()):
                combined.append(words[i] + words[i + 1])
                i += 1

                if i == len(words) - 1:
                    last_punct = True
            else:
                combined.append(words[i])
        i += 1
    
    if not last_punct:
        combined.append(words[i])

    return combined
