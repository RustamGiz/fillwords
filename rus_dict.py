words = []

with open('russian_nouns.txt', 'r', encoding='utf-8') as f:
    for line in f:
        words.append(line.strip())

print(len(words))

substr = 'йар'

print(len([word for word in words if substr in word]))
