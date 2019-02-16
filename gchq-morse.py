#!/usr/bin/env python3

"""
GCHQ placed a plaque for their first centenary, with two different codes:
https://www.instagram.com/p/Bt5v_YrlDhz/

The first code is simple: just read characters with dot or dash under them.
The result is "1 hundred years".

The second one is a bit harder: the dots are dashes are a morse code, but there
are no separators, so there are many possible solutions. The code below
searches for all of them, checks which ones are English words, and prints the
solutions (as it turns out, there is only one).
"""

import enchant


morse = {
    "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.",
    "g": "--.", "h": "....", "i": "..", "j": ".---", "k": "-.-", "l": ".-..",
    "m": "--", "n": "-.", "o": "---", "p": ".--.", "q": "--.-", "r": ".-.",
    "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-",
    "y": "-.--", "z": "--..",
    "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
    "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----",
}
dict_en = enchant.Dict("en_UK")


def decode(s, result="", morse_res=""):
    """
    Decode string `s` containing (only) dots and dashes.

    :param s: Input string.
    """
    if s:
        for char, code in morse.items():
            if s.startswith(code):
                decode(s[len(code):], f"{result}{char}", f"{morse_res}{code}|")
    elif dict_en.check(result):
        print(f"{result} [{morse_res.strip('|')}]")


decode("....-.-..-..-")
