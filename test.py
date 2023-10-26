print("Code:")
lines = []
while True:
    line = input("")
    if line:
        lines.append(line)
    else:
        break
text = '\n'.join(lines)


print("\n")

print(text.replace("\\n", "\\\\n"))

"""
def extract_words(word, letter):
    words_list = []
    for w in word.split():
        if w[0] == letter:
            words_list.append(w)
    return words_list
if __name__ == '__main__':
    words = 'This is a sample sentence to test the program'
    letter = 's'
    print(extract_words(words, letter))
"""




