s = "us to remember that life 's ultimately a gamble and last orders are to aren't can't"

def tokenize(s)
    combined = []
    words = s.split(' ')
    i = 0
    while i < len(words) - 1:
        if i != len(words) - 1:
            if(not words[i+1][0].isalpha()):
                combined.append(words[i] + words[i + 1])
                i += 1
            else:
                combined.append(words[i])
        i += 1

    combined.append(words[i])

print(combined)

