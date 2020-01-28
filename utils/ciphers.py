import string

from itertools import cycle
ASCII_a = 97


def shift_letter(char, offset):
    if char not in string.ascii_letters:
        return char
    idx = ord(char.lower()) - ASCII_a
    new_idx = (idx + offset) % 26
    new_char = chr(ASCII_a + new_idx)
    if char.isupper():
        return new_char.upper()
    else:
        return new_char


def caesar_shift(text, offset):
    """
    Performs a Caesar shift by the given offset.

    If the offset is a letter, it will look it up in the alphabet to convert
    it to a shift. (For example, a shift of 'C' means that 'A' goes to 'C',
    which is the same as a shift of 2.)
        
        >>> print(caesar_shift('caesar', 13))
        pnrfne
        >>> print(caesar_shift('CAESAR', 'C'))
        ECGUCT

    """
    if isinstance(offset, str):
        offset = ord(offset.lower()) - ASCII_a

    shifted = [shift_letter(ch, offset) for ch in text]
    return ''.join(shifted)


def caesar_unshift(text, offset):
    """
    Performs a Caesar shift backwards by the given offset.
    
    If the offset is a letter, it will look it up in the alphabet to convert
    it to a shift. (For example, a shift of 'C' means that 'C' goes to 'A',
    which is the same as a backward shift of 2.)

        >>> print(caesar_unshift('DBFTBS TIJGU', 1))
        CAESAR SHIFT
    """
    if isinstance(offset, str):
        offset = ord(offset.lower()) - ASCII_a
    return caesar_shift(text, -offset)


def vigenere_encode(text, key, one_based=False):
    """
    Apply the Vigenere cipher to `text`, with `key` as the key.

    In this cipher, A + A = A, but in many cases in the Mystery Hunt,
    A + A = B. To get the A + A = B behavior, set `one_based` to true.

    >>> vigenere_encode('ABRACADABRA', 'abc')
    'ACTADCDBDRB'
    >>> vigenere_encode('ABRACADABRA', 'abc', one_based=True)
    'BDUBEDECESC'
    """
    shifted = []
    letters = [ch for ch in text if ch in string.ascii_letters]
    shifted = [caesar_shift(ch, shift)
               for (ch, shift) in zip(letters, cycle(key))]
    result = ''.join(shifted)
    if one_based:
        result = caesar_shift(result, 1)
    return result


def vigenere_decode(text, key, one_based=False):
    """
    Decode a Vigenere cipher on `text`, with `key` as the key.

    In this cipher, B - B = A, but in many cases in the Mystery Hunt,
    B - B = Z. To get the B - B = Z behavior, set `one_based` to true.

    >>> vigenere_decode(vigenere_encode('ABRACADABRA', 'abc'), 'abc')
    'ABRACADABRA'
    """
    shifted = []
    letters = [ch for ch in text if ch in string.ascii_letters]
    shifted = [caesar_unshift(ch, shift)
               for (ch, shift) in zip(letters, cycle(key))]
    result = ''.join(shifted)
    if one_based:
        result = caesar_shift(result, -1)
    return result


PHONESPELL_MAP = dict(zip(
    'abcdefghijklmnopqrstuvwxyz',
    '22233344455566677778889999'
))
UN_PHONESPELL_MAP = {
    '2': '[abc]',
    '3': '[def]',
    '4': '[ghi]',
    '5': '[jkl]',
    '6': '[mno]',
    '7': '[pqrs]',
    '8': '[tuv]',
    '9': '[wxyz]'
}


def phonespell(text):
    "Convert letters to the digits 2-9 on a phone keypad."
    return ''.join(PHONESPELL_MAP[ch] for ch in slugify(text))


def un_phonespell(digits):
    """
    Convert digits 2-9 to a regular expression of letters, matching what
    they spell on a phone keypad.
    """
    if isinstance(digits, int):
        digits = str(digits)
    pattern = ''.join(UN_PHONESPELL_MAP[digit] for digit in digits)
    return pattern
