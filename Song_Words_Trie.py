"""
Name: Teng Ian Khoo
Created: 3rd October 2019
Last Modified: 11th October 2019
"""
# imported regex library for use
import re as re


# A Basic trie Data Structure Class
class Trie():
    def __init__(self):
        self.root = Node()

    def search_lookup(self, word):
        current = self.root
        return self.search_lookup_aux(current, word, 0)

    def search_lookup_aux(self, current, word, i=0):
        # our base case
        if len(word) == i:
            # if word not found
            if current.child[26] is None:
                return False
            return current.child[26].data
        # recursive basis
        else:
            index = ord(word[i]) - 97
            i += 1
            # case for if the letter is not in the Trie
            if current.child[index] is None:
                return False
            return self.search_lookup_aux(current.child[index], word, i)

    def insert_lookup(self, word, data, counter=None):
        current = self.root
        song_counter = counter
        self.insert_lookup_aux(current, word, data, 0, song_counter)

    def insert_lookup_aux(self, current, word, data, i=0, song_counter=None):
        # Our base case
        if len(word) == i:
            # case for if a new word is inserted to the Trie , creation of our $
            if current.child[26] is None:
                current.child[26] = Node()
                current.child[26].unique_song_check = song_counter
                current.child[26].data.append(data)
            # case for if a duplicate word is found, but the song_id differs
            if song_counter is not None:
                # we will only update the data in our Trie, if the word comes from a different song
                if current.child[26].unique_song_check != song_counter:
                    current.child[26].data.append(data)
                    current.child[26].unique_song_check = song_counter
        # we reach the ends
        # do normal $ sign stuff
        else:
            index = ord(word[i]) - 97
            if current.child[index] is None:
                current.child[index] = Node()
            i += 1
            self.insert_lookup_aux(current.child[index], word, data, i, song_counter)

    def search_most_common(self, word):
        current = self.root
        return self.search_most_common_aux(current, word, 0)

    def search_most_common_aux(self, current, word, i=0):
        # our base case
        if len(word) == i:
            # else we iterate down our Trie until we reach the maximum end node
            word_found = False
            # we know that the word is a prefix, hence a suffix must exist for it, so we will loop until we find one
            while not word_found:
                # our .data now contains the index in which we will find the path to our most frequent word
                index = current.data
                if current.child[26] is not None:
                    if current.child[26].count == current.maximum:
                        # we have found the word
                        return current.child[26].data
                # if we don't find the word we will go to our next child node
                current = current.child[index]
        # recursive basis
        else:
            index = ord(word[i]) - 97
            i += 1
            # case for if the letter is not in the Trie
            if current.child[index] is None:
                return False
            return self.search_most_common_aux(current.child[index], word, i)

    def insert_common_word(self, word, counter=None):
        current = self.root
        song_counter = counter
        self.insert_common_word_aux(current, word, 0, song_counter)

    def insert_common_word_aux(self, current, word, i=0, song_counter=None):
        # Our base case
        if len(word) == i:
            # case for if a new word is inserted to the Trie , creation of our $
            if current.child[26] is None:
                current.child[26] = Node()
                current.child[26].unique_song_check = song_counter
                # update the count for the number of times the word has appeared in different lines
                current.child[26].count += 1
                # save the data of the word at the Last Node
                current.child[26].data = word
                # case for if a duplicate word is found, but the song_id differs
            # we will only update the data in our Trie, if the word comes from a different song
            if current.child[26].unique_song_check != song_counter:
                current.child[26].count += 1
                current.child[26].unique_song_check = song_counter
            # set the maximum of the leaf node to the count (only time we enter this is when we see a new song_id)
            current.child[26].maximum = current.child[26].count

            # We check to see if the maximum of the leaf node is greater than the maximum of the current node
            if current.child[26].maximum > current.maximum:
                # if it is we have a new most common word and must update the path on our recursion back
                current.maximum = current.child[26].maximum
        # we reach the ends
        # do normal $ sign stuff
        else:
            index = ord(word[i]) - 97
            # creation of our trie word node
            if current.child[index] is None:
                current.child[index] = Node()
            i += 1
            self.insert_common_word_aux(current.child[index], word, i, song_counter)
            # after we have inserted the word, we check if the frequency of the end node is bigger than any previous
            if current.child[index].maximum > current.maximum:
                current.maximum = current.child[index].maximum
                # if the maximum has been updated, that means that we have a new maximum word, so we need to save
                # the index for easier retrieval
                current.data = index

    def insert_suffix(self, word):
        current = self.root
        # insert every suffix of the word
        for i in range(len(word)):
            self.insert_suffix_aux(current, word, 0, i)

    def insert_suffix_aux(self, current, word, i=0, letter_index=0):
        # Base case
        if len(word) == letter_index + i:
            if current.child[26] is None:
                current.child[26] = Node()
        # Recursive Base
        else:
            # we need to insert the word without slicing , the string so we add the i to our start
            index = ord(word[letter_index + i]) - 97
            # creation of our trie word node
            if current.child[index] is None:
                current.child[index] = Node()
            i += 1
            self.insert_suffix_aux(current.child[index], word, i, letter_index)


class Node():
    def __init__(self, size=27):
        self.data = []
        self.child = [None] * size
        self.unique_song_check = None
        self.count = 0
        self.maximum = 0


def lookup(data_file, query_file):
    # The Trie that we are to populate with the words from our data_file
    word_trie = Trie()
    # This is a counter to keep track of the current song id/line we are looking at, that is because we don't care
    # about duplicate words in the same song
    unique_song_counter = 0

    # Reading all the words of the data_file and adding the words to our Trie
    with open(data_file, "r") as file:
        # split each line in the file into an array of [song_id,word_1,word_2......, word_n]
        for line in file:
            words_in_song = re.split('[ :]', line.strip())
            # for each word in the Song, we will add it to our Trie
            for i in range(1, len(words_in_song)):
                word_trie.insert_lookup(words_in_song[i], words_in_song[0], unique_song_counter)
            unique_song_counter += 1

    # Now that our Trie is populated, we can open through our query file and try to search through our Trie for the
    # words and their corresponding Song_id

    # open up the song_ids text file for us to write into it later
    write_file = open("song_ids.txt", "w+")

    # opening up the query file to find what we have to search for
    with open(query_file, "r") as file:
        for line in file:
            # get the word of the query
            word = line.strip()
            # Now to search our Trie for the word, will return False or a list of song_ids
            result = word_trie.search_lookup(word)
            # if the word is not found we need to write "Not found"
            if not result:
                write_file.write("Not found")
                write_file.write("\n")
            else:
                # join my array to a string using string.join , based on the documentation found at
                # https://docs.python.org/3/library/stdtypes.html#str.join it is faster than string concatenation
                song_ids = " ".join(str(item) for item in result)
                write_file.write(song_ids)
                write_file.write("\n")

    # Remember to close the file
    write_file.close()


def most_common(data_file, query_file):
    # The Trie that we are to populate with the words from our data_file
    word_trie = Trie()
    # This is a counter to keep track of the current song id/line we are looking at, that is because we don't care
    # about duplicate words in the same song
    unique_song_counter = 0

    # Reading all the words of the data_file and adding the words to our Trie
    with open(data_file, "r") as file:
        # split each line in the file into an array of [song_id,word_1,word_2......, word_n]
        for line in file:
            words_in_song = re.split('[ :]', line.strip())
            # for each word in the Song, we will add it to our Trie
            for i in range(1, len(words_in_song)):
                word_trie.insert_common_word(words_in_song[i], unique_song_counter)
            unique_song_counter += 1

        # Now our Trie is populated, we need to open our write file and our query file and recurse through our string
        # for the word

        # open up the song_ids text file for us to write into it later
        write_file = open("most_common_lyrics.txt", "w+")

        # opening up the query file to find what we have to search for
        with open(query_file, "r") as file:
            for line in file:
                # get the word of the query
                word = line.strip()
                # Now to search our Trie for the word, will return False or a list of song_ids
                result = word_trie.search_most_common(word)
                # if the word is not found we need to write "Not found"
                if not result:
                    write_file.write("Not found")
                    write_file.write("\n")
                else:
                    write_file.write(result)
                    write_file.write("\n")

        # Remember to close the file
        write_file.close()


def palindromic_substrings(S):
    # I now will create a suffix Trie for the reverse of the word
    # Reverse of a String Using the .join operator because it is more efficient than slicing
    str_list = []
    # Generate a stack of the reverse word
    for i in range(len(S) - 1, -1, -1):
        str_list.append(S[i])
    reverse_word = "".join(str_list)

    # Generate our Reverse Trie
    reverse_trie = Trie()
    reverse_trie.insert_suffix(reverse_word)

    # create the list that will store the tuples of the starting and end indexes
    substrings = []

    # Now to once again loop through my all the suffixes of my words, if the word is a palindrome, it must be found
    # in my Trie
    for i in range(len(S)):
        current_node = reverse_trie.root
        letter_index = i
        palindrome_found = False
        # create two, stacks, one for our the word we are looking at, and one for our reverse Trie
        word_list = []
        reverse_list = []
        # loop through, my reverse Trie
        while letter_index < len(S) and not palindrome_found:
            letter = S[letter_index]
            trie_index = ord(letter) - 97
            if current_node.child[trie_index] is None:
                palindrome_found = True
            else:
                # append the word to our word list
                word_list.append(letter_index)
                current_node = current_node.child[trie_index]
                letter_index += 1
        # we now should populate our reverse_list with the reverse of the word list
        for z in range(len(word_list) - 1, -1, -1):
            reverse_list.append(word_list[z])
        # after our while loop, we should have both stacks with similar items, however there may be cases where it is
        # not a palindrome, hence we need to do a check on the stacks
        is_palindrome = True
        # we only care about 2 > words
        if len(word_list) >= 2:
            for _ in range(len(word_list)):
                word = S[word_list.pop()]
                reverse = S[reverse_list.pop()]
                if word != reverse:
                    is_palindrome = False
            if is_palindrome:
                substrings.append((i, letter_index - 1))
            # if it isn't a palindrome then we need to just remove the last alphabet, remember that it is
            # part of a bigger palindrome, and as we are searching from the largest suffix to the smallest, we will
            # always find the larger suffix first
            elif not is_palindrome and (letter_index - i - 2) >= 2:
                substrings.append((i, letter_index - 2))
    return substrings



