def encrypt_ceasar(word, key):
    result = ''
    for letter, k in zip(word, key):
        shift = dct[k.lower()]
        new_letter = 65 + (ord(letter) - 65 + shift) % 26
        result += chr(new_letter)
    return result

def decrypt_ceasar(word, key):
    result = ''
    for letter, k in zip(word, key):
        shift = dct[k.lower()]
        new_letter = 65 + (ord(letter) - 65 - shift) % 26
        result += chr(new_letter)
    return result

def adeq(word, key):
    size_word = len(word)
    while len(key) < size_word:
        key += key
    return key


dct = {}
start, end = ord('a'), ord('z')+1
for i in range(start, end):
    dct[chr(i)] = i - start

print('Что вы хотите сделать? (0 - зашифровать; 1 - расшифровать)')
act = int(input())
word = input('Введите слово: ')
key = input('Введите ключ: ')
new_key = adeq(word, key)

if act == 0:
    print('Зашифрованное слово:', encrypt_ceasar(word, new_key))
else:
    print('Расшифрованное слово:', decrypt_ceasar(word, new_key))