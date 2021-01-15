a = 6
b = 3
print(a / b)

help(print)

print(min(1, 2, 3))

jack_age = 23
alex_age = 42
lana_age = 34
print(min(jack_age, alex_age, lana_age))

x = 5
y = 10
result = sum([x, y])
print(result)

budget_net = 100 * 3000 / 123
price_net = 100 * 12000 / 123
print(budget_net)
print(price_net)
print(price_net - budget_net)




hero_damage = 100


def double_damage():
    global hero_damage
    hero_damage *= 2


def disarmed():
    global hero_damage
    hero_damage /= 10


def power_potion():
    global hero_damage
    hero_damage =+ 100


# a = int(input())
# b = int(input())
# hours = int(input())
#
# if hours < a:
#     print("Deficiency")
# elif hours > b:
#     print("Excess")
# elif a <= hours <= b:
#     print("Normal")

print("Asd")

print(25 * 2 % 100 >= 50)

x = 25
while x * 2 % 100 >= 50:
    print(x)
    x += 3

print("Asd")

x = 25
while x <= 30:
    print(x)
    x += 3

print("Asd")
x = 25
while x % 2 != 0:
    print(x)
    x += 3

# print("Asd")
# x = 25
# while x > 0:
#     print(x)
#     x += 3