def processing(number):
    digit = str(number)
    if len(digit) == 1:
        return to_emoji(digit)
    elif len(digit) == 2:
        return to_emoji(digit[0])+to_emoji(digit[1])


def to_emoji(number):
    if number == '0':
        return '0️⃣'
    elif number == '1':
        return '1️⃣'
    elif number == '2':
        return '2️⃣'
    elif number == '3':
        return '3️⃣'
    elif number == '4':
        return '4️⃣'
    elif number == '5':
        return '5️⃣'
    elif number == '6':
        return '6️⃣'
    elif number == '7':
        return '7️⃣'
    elif number == '8':
        return '8️⃣'
    elif number == '9':
        return '9️⃣'
