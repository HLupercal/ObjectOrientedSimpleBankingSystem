string = "red yellow fox bite orange goose beeeeeeeeeeep"
vowels = 'aeiou'

total = 0

for vowel in vowels:
    for letter in string:
        if letter == vowel:
            total += 1

print(total)

#alternative
total = 0

for letter in string:
    if letter in vowels:
        total += 1

print(total)
