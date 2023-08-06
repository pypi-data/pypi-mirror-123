import fire
import pyperclip as pc


def encrypt(encode: str, amount: int, copy: bool = False):
    final = ""
    for character in encode:
        final += chr(ord(character) + amount)

    if copy:
        pc.copy(final)
    return final


def decrypt(encode: str, amount: int, copy: bool = False):
    final = ""
    for character in encode:
        final += chr(ord(character) - amount)

    if copy:
        pc.copy(final)
    return final


command_index = \
    {
        "encrypt": encrypt,
        "enc": encrypt,
        "e": encrypt,

        "decrypt": decrypt,
        "dec": decrypt,
        "d": decrypt,
    }
fire.Fire(command_index)