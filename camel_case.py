
word = "javaIsNeat"
previous = ''
result = ''
for letter in word:
    if letter.islower():
        result += letter
    if letter.isupper() and previous and previous.islower:
        result = result + "_" + letter.lower()
    previous = letter

print(result)



class Turtle:
    def __init__(self, x, y):
        # the initial coordinates of the turtle
        self.x = x
        self.y = y

    def move_up(self, n):
        self.y += n

    def move_down(self, n):
        self.y = 0 if n > self.y else self.y - n

    def move_right(self, n):
        self.x += n

    def move_left(self, n):
        self.x = 0 if n > self.x else self.x - n


leo = Turtle(1, 1)
leo.move_up(7)
leo.move_left(5)
leo.move_down(4)
leo.move_right(6)

print("{} {}".format(leo.x, leo.y))


cents = 299

print(cents % 100)
print(cents // 100)

# while cents % 100 != 0:
#     cents


class PiggyBank:
    # create __init__ and add_money methods
    def __init__(self, dollars, cents):
        self.dollars = dollars
        self.cents = cents

    def add_money(self, deposit_dollars, deposit_cents):
        self.dollars += deposit_dollars + deposit_cents // 100
        self.cents += deposit_cents % 100

bank = PiggyBank
