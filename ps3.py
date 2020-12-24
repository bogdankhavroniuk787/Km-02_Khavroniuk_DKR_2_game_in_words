# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : < Bohdan Khavroniuk >
# Time spent    : <6-7 hours>
# do not judge strictly please , I dont now that 4th problem is correct so I map it like unmade


import copy
import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words(2).txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	


#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word_length = len(word.lower())
    first_m = 0
    for i in word.lower():
        if i != ('*'):
            first_m += SCRABBLE_LETTER_VALUES[i]
    second_m = max(1, 7 * word_length - 3 * (n - word_length))
    score =  first_m * second_m
    return score


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')
    print()


# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    x = '*'
    hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


# Problem #2:

def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    hand_update = hand.copy()
    word = word.lower()
    for letter in word:
        if letter in hand:
            hand_update[letter] = hand_update[letter] - 1
            if hand_update[letter] < 0:
                hand_update[letter] = 0
        else :
            continue

    return hand_update


#
# Problem #3:
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word = word.lower()
    if word in word_list:
        for litter in word:
            if (litter not in hand.keys()) or word.count(litter) > hand[litter]:
                return False
        else:
            return True
    elif "*" in word:
        for vowel in VOWELS:
            if word.replace("*", vowel) in word_list:
                return True
        else:
            return False

    else:
        return False


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """

    return sum(hand.values())


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    total_score = 0
    while True:
        print("Current hand:")
        display_hand(hand)
        print("Enter word or for count, or '!!' for finish:")
        word = input()
        word = word.lower()
        if word != "!!":
            if is_valid_word(word, hand, word_list) == True:
                n =len(hand)
                total_score += get_word_score(word, n)
                hand = update_hand(hand, word)
                n = calculate_handlen(hand)
                if n == 0:
                    print("hand is empty")
                    break
                else:
                    continue
            else:
                hand = update_hand(hand, word)
                n = calculate_handlen(hand)
                print("invalid word")
                if n == 0:
                    print("hand is empty")
                    break
                else:
                    continue
        else:
            break

    return  total_score


# Problem #6: Playing a game

# procedure you will use to substitute a letter in a hand

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    vovels = VOWELS + CONSONANTS
    coppyied_hand = copy.copy(hand)
    for i in coppyied_hand.keys():
        vovels = vovels.replace(i, '')
        if i == letter:
            hand[random.choice(vovels)] = hand.pop(i)
            break
    return hand
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    while True:
        print("Enter total number of hands:")
        hands = input()
        try:
            hands = int(hands)
            if hands <= 0:
                print("Oops number is incorrect please, enter the correct number")
                continue
            else:
                break
        except ValueError:
            print("You are entered not int")
            continue
    total_hands_score = 0
    a = 0
    while a < hands:
        print("-" * 20)
        n = HAND_SIZE
        hand = deal_hand(n)
        while True:
            display_hand(hand)
            while True:
                try:
                   user_input = str(input("Would you like to substitute a letter?(yes or no)"))
                   user_input =user_input .lower()
                   if user_input == "yes" or user_input == "no" :
                     break
                except ValueError:
                    print("Please input string")
            if user_input == "yes":
                print("Which letter would you like to replace:")
                while True:
                    while True:
                       try:
                          letter = str(input())
                          break
                       except ValueError:
                           print("You are entered not str ")
                    letter = letter.lower()
                    if len(letter) != 1:
                        print("wright only one  letter please")
                        continue
                    elif letter not in hand:
                        print("hand not include this letter")
                    else:
                        hand = substitute_hand(hand, letter)
                        break
                break
            elif user_input  == "no":
                break
        total_hands_score += play_hand(hand, word_list)
        a += 1
    print("=" * 20)
    print("Total score over all hands: {} points".format(total_hands_score))
    print("THE END , created by Khavroniuk B. A.")

    



if __name__ == '__main__':
    print("Welcome in game")
    word_list = load_words()
    play_game(word_list)
