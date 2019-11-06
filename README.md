# Song_Words_Trie
The same problem as the song Words algorithm in my Git, however instead of using a Radix Sort, we are using a Data Structure called a Trie for efficient String retrieval.


LOOKUP
What we want is to insert the words from our data_file into a Trie, but what should happen is that only words duplicate words that come from a different song should be entered into the Trie, to do this my data attribute was a list that contained all the song)ids that the word was found in, and I used another attribute called unique_song_check to do so. At ebery line of my data_file, I inserted the word with a additional parameter which kept track of what song_id I was inserting from my file, and if I passed a node and the unique_song_check was different from the parameter, I knew that the word was a duplicate but from a different song and hence will append it song_id to my data attribute.
The insertion is done in O(Ci), where CI is the number of characters in data_file. This is because we have to read all the words from the data_file, and add it to our Trie.
Now that my Trie was populated with all the words, I opened my query file and recurse through my Trie, if we successfully recursed through my Trie (the Trie.child[word_index] was found for the length of the whole word) then I would return my data attribute from the child[26] Node.
The Search is done in O(Cq) where CQ is the number of characters in query_file, this is because we have to search our Trie through all the words in our query file, doing so will will take the length of the whole string if it is in our Trie, or less if it is not in our Trie
Writing to the file will take O(Cp) where CP is the number of characters in song_ids.txt , this is because writing is an output sensitive complexity, and depends on how many song_ids the word has been found in.
Hence overall lookup runs in:
O(CI + CQ + CP ), where O(CI + CQ + CP ), where • CI is the number of characters in data_file
• CQ is the number of characters in query_file
• CP is the number of characters in song_ids.txt
MOST_COMMON
When we insert the word into our string, this time we are incrementing the count attribute of the nodes, however we will only increment the count attribute if the words is found in a different song, we do this checking similarly to how we do it in question 1. To find the most common word in the Trie for a given prefix, what we make use of is the maximum attribute of the Node, this maximum attribute will be updated each time a word is inserted or updated(found in another song_id), this essentially gives us a path from the current node to the node containing the most frequent word as we can compare the maximum and count attributes of the Nodes.
  
We save the whole word at the data attribute, but only at the termination node ( the $ Node). We otherwise save the index where the most frequent word occurs into our data attribute, this coupled with the count and maximum attributes allows us to find the path to the most_frequent end node is O(n) time.
When we are searching for the most common word, we recurse until the end of the word, then if the word to search for is already a word, we check the termination node and compare the count and maximum attributes if it is the same we can just return the word.
Else the word is a prefix of one of our words, and we will loop through the rest of the Nodes using the data attribute to know which child path to take, and once we reach the termination Node, we just return the data attribute of the word.
Overall most_common runs in:
O(CI + CQ + CM ), where
• CI is the number of characters in data_file
• CQ is the number of characters in query_file
• CM is the number of characters in most_common_lyrics.txt
PALINDROMIC_SUBSTRINGS
I was unable to get full functionality for this function, what I did was build a Trie of the reverse word we are asked to search for.
If the word is a palindrome we should be able to find the word by traversing our Trie, during which we are appending the letter_index we are looking at into a stack, when we reach a letter where we are unable to find the next Node for, it means that we have found our palindrome.
However we are not sure if it is a palindrome yet, we build a stack which contains the reverse of the word_stack and compare the word[index] from both stacks when we pop from them. If the word matches for the whole length of the word, it is a palindrome. If it doesn’t then it means that it is part of a larger palindrom, and since we are searching through our Trie in the order of howe we built it. We would have found the larger palindrome already, and we just need to remove the last letter to make it a palindrome.
Overall it should run in:
O(N2) where N is the length of S.
