import re
file = open('example.txt', 'r', encoding='utf-8')
content = file.read()
words = re.findall(r'\b\w+\b', content)
max_length = max(len(word) for word in words)
max_length_words = []
for word in words:
    if len(word) == max_length:
        max_length_words.append(word)
for word in max_length_words:
    print(word)
file.close()