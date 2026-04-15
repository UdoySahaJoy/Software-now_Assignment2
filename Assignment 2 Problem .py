raw_file = "raw_text.txt"
encrypted_file = "encrypted_text.txt"
decrypted_file = "decrypted_text.txt"
key_file = "key.txt"


def shift_letter(ch, shift, base):
    position = ord(ch) - ord(base)
    new_position = (position + shift) % 26
    return chr(ord(base) + new_position)

def encrypt_text(text, shift1, shift2):
    encrypted = ""
    key_data = ""

    for ch in text:
        if 'a' <= ch <= 'm':
            encrypted += shift_letter(ch, shift1 * shift2, 'a')
            key_data += "1"

        elif 'n' <= ch <= 'z':
            encrypted += shift_letter(ch, -(shift1 + shift2), 'a')
            key_data += "2"

        elif 'A' <= ch <= 'M':
            encrypted += shift_letter(ch, -shift1, 'A')
            key_data += "3"

        elif 'N' <= ch <= 'Z':
            encrypted += shift_letter(ch, shift2 ** 2, 'A')
            key_data += "4"

        else:
            encrypted += ch
            key_data += "0"

    return encrypted, key_data


def decrypt_text(text, key_data, shift1, shift2):
    decrypted = ""

    for i in range(len(text)):
        ch = text[i]
        code = key_data[i]

        if code == "1":
            decrypted += shift_letter(ch, -(shift1 * shift2), 'a')

        elif code == "2":
            decrypted += shift_letter(ch, shift1 + shift2, 'a')

        elif code == "3":
            decrypted += shift_letter(ch, shift1, 'A')

        elif code == "4":
            decrypted += shift_letter(ch, -(shift2 ** 2), 'A')

        else:
            decrypted += ch

    return decrypted