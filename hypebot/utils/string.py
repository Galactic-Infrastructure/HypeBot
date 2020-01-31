import math
import random
import re
from pathlib import Path

from .path import wordlist_path
from .normalize import slugify


ASCII_a = 97

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

LOWERCASE_VOWELS = 'aeiou'
LOWERCASE_CONSONANTS = 'bcdfghjklmnpqrstvwxyz'

# An estimate of the frequencies of letters in English, as a length-26
# vector of proportions
LETTER_FREQS = [
    0.08331452,  0.01920814,  0.04155464,  0.03997236,  0.11332581,
    0.01456622,  0.02694035,  0.02517641,  0.08116646,  0.00305369,
    0.00930784,  0.05399477,  0.02984008,  0.06982714,  0.06273243,
    0.0287359 ,  0.00204801,  0.07181286,  0.07714659,  0.06561591,
    0.03393991,  0.01232891,  0.01022719,  0.0037979 ,  0.01733258,
    0.00303336
]

# Loaded only if needed.
# Use 'get_bigram_freqs' and 'get_trigram_freqs' to access these.
BIGRAM_FREQS = []

TRIGRAM_FREQS = []


def letters_to_vec(letters):
    """
    Convert an iterator of lowercase letters, such as a 'slug' form, into
    a length-26 vector indicating how often those letters occur.
    """
    vec = [0] * 26
    for letter in letters:
        index = ord(letter) - ASCII_a
        vec[index] += 1
    return vec


def to_proportion(vec):
    """
    Convert a vector that counts occurrences to a vector of proportions
    (whose sum is 1).
    """
    vecsum = sum(vec)
    return [value / vecsum for value in vec]


def alphagram(slug):
    """
    Given text in 'slug' form, return its alphagram, which is the string of
    its letters sorted in alphabetical order.
    """
    return ''.join(sorted(slug))


def alphabytes(slug):
    """
    This representation is used internally to Solvertools. It's like an
    alphagram, but represents up to 7 occurrences of a letter as unique bytes
    that can be searched for in a specially-prepared word list.

    This allows simple regexes to match "a word with at most two e's and at
    most three t's", a search which would be very complex and inefficient in
    the usual string representation.
    """
    alpha = alphagram(slug)
    current_letter = None
    rank = 0
    bytenums = []
    for letter in alpha:
        if letter == current_letter:
            rank += 1
        else:
            rank = 0
        if rank < 6:
            num = ord(letter) - 96 + (rank + 2) * 32
        else:
            num = ord(letter) - 96
        bytenums.append(num)
        current_letter = letter
    return bytes(bytenums)


def alphabytes_to_alphagram(abytes):
    """
    Convert the specialized 'alphabytes' form described above to an ordinary,
    printable alphagram.
    """
    letters = [chr(96 + byte % 32) for byte in abytes]
    return ''.join(letters)


def anagram_diff(a1, a2):
    """
    Find the difference between two multisets of letters, in a way specialized
    for anagramming.

    Returns a pair containing:

    - the alphagram of letters that remain
    - the number of letters in a2 that are not found in a1, which is the number
      of "wildcards" to consume
    """
    adiff = ''
    wildcards_used = 0
    for letter in set(a2) - set(a1):
        diff = a2.count(letter) - a1.count(letter)
        wildcards_used += diff
    for letter in sorted(set(a1)):
        diff = (a1.count(letter) - a2.count(letter))
        if diff < 0:
            wildcards_used -= diff
        else:
            adiff += letter * diff
    return adiff, wildcards_used


def diff_both(a1, a2):
    """
    Compare two multisets of letters, returning:

    - The alphagram of letters in a1 but not in a2
    - The alphagram of letters in a2 but not in a1
    """
    diff1 = ''
    diff2 = ''
    for letter in set(a2) - set(a1):
        diff = a2.count(letter) - a1.count(letter)
        diff2 += letter * diff
    for letter in sorted(set(a1)):
        diff = (a1.count(letter) - a2.count(letter))
        if diff < 0:
            diff2 += letter * diff
        else:
            diff1 += letter * diff
    return diff1, diff2


def diff_exact(full, part):
    """
    Find the difference between two multisets of letters, returning the
    alphagram of letters that are in `full` but not in `part`. If any letters
    are in `part` but not in `full`, raises an error.
    """
    diff1, diff2 = diff_both(full, part)
    if diff2:
        raise ValueError("Letters were left over: %s" % diff2)
    return diff1


def anahash(slug):
    if slug == '':
        return ''
    vec = to_proportion(letters_to_vec(slug))
    anomalies = []
    for i in range(26):
        if vec[i] > LETTER_FREQS[i]:
            anomalies.append(i + ASCII_a)
    return bytes(list(anomalies)).decode('ascii')


def anagram_cost(letters):
    """
    Return a value that's probably larger for sets of letters that are
    harder to anagram.

    I came up with this formula in the original version of anagram.js. Much
    like most of anagram.js, I can't entirely explain why it is the way it
    is.

    The 'discrepancy' of a set of letters is a vector indicating how far
    it is from the average proportions of a set of letters. These values
    are raised to the fourth power and summed to form one factor of this
    cost formula. The other factor is the number of letters.
    """
    if letters == '':
        return 0
    n_letters = len(letters)
    vec = to_proportion(letters_to_vec(letters))
    sq_cost = 0.0
    for i in range(26):
        discrepancy = (vec[i] / LETTER_FREQS[i] - 1) ** 2
        sq_cost += discrepancy
    return sq_cost ** 0.5 * n_letters


VOWELS_RE = re.compile('[aeiouy]')
def consonantcy(slug):
    """
    Given a word in 'slug' form, return just the consonants. 'y' is always
    considered a vowel and 'w' is always considered a consonant, regardless
    of context.
    """
    return VOWELS_RE.sub('', slug)


def random_letters(num):
    """
    Get `num` random letters that are distributed like English. Useful for
    testing against a null hypothesis.
    """
    letters = []
    for i in range(num):
        rand = random.random()
        choice = '#'
        for j in range(26):
            if rand < LETTER_FREQS[j]:
                choice = chr(j + ord('a'))
                break
            else:
                rand -= LETTER_FREQS[j]
        letters.append(choice)
    return ''.join(letters)


def only_vowels(word, preserve_spaces=False):
  return ''.join([k for k in word if k in LOWERCASE_VOWELS \
                                  or (preserve_spaces and k == ' ')])


def only_consonants(word, preserve_spaces=False):
  return ''.join([k for k in word if k not in LOWERCASE_VOWELS \
                                  or (preserve_spaces and k == ' ')])


def get_bigram_freqs():
    global BIGRAM_FREQS
    if not BIGRAM_FREQS:
        BIGRAM_FREQS = [[-1000 for _ in range(26)] for _ in range(26)]
        total_bigrams = 0
        with open(wordlist_path('letter_bigrams.txt'), 'r') as fd:
            lines = [l.split(' ') for l in fd.readlines()]

        for line in lines:
            bigram, freq = line
            total_bigrams += int(freq)

        for line in lines:
            line[1] = math.log(int(line[1]) / total_bigrams)
            ch1 = ord(line[0][0].lower()) - ord('a')
            ch2 = ord(line[0][1].lower()) - ord('a')
            BIGRAM_FREQS[ch1][ch2] = line[1]

    return BIGRAM_FREQS


def get_trigram_freqs():
    global TRIGRAM_FREQS
    if not TRIGRAM_FREQS:
        TRIGRAM_FREQS = [[[-1000 for _ in range(26)] for _ in range(26)] for _ in range(26)]
        total_trigrams = 0
        with open(wordlist_path('letter_trigrams.txt'), 'r') as fd:
            lines = [l.split(' ') for l in fd.readlines()]

        for line in lines:
            trigram, freq = line
            total_trigrams += int(freq)

        for line in lines:
            line[1] = math.log(int(line[1]) / total_trigrams)
            ch1 = ord(line[0][0].lower()) - ord('a')
            ch2 = ord(line[0][1].lower()) - ord('a')
            ch3 = ord(line[0][2].lower()) - ord('a')
            TRIGRAM_FREQS[ch1][ch2][ch3] = line[1]

    return TRIGRAM_FREQS
