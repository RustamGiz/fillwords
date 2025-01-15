words = []

with open('zdf.txt', 'r', encoding='utf-8') as f:
    for line in f:
        words.append(line.strip())

print(len(words))

substr = 'а'

print(len([word for word in words if substr in word]))
