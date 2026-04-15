raw_file = "raw_text.txt"
encrypted_file = "encrypted_text.txt"
decrypted_file = "decrypted_text.txt"
key_file = "key.txt"


def shift_letter(ch, shift, base):
    position = ord(ch) - ord(base)
    new_position = (position + shift) % 26
    return chr(ord(base) + new_position)