import os
import re
import numpy as np

from final_project.data import load_words, load_vectors


class WordEmbedding(object):
    def __init__(self, words, vecs):
        self.words = words
        self.words = {w: self.words.index(w) for w in self.words}
        self.vecs = vecs

    def __call__(self, word):
        """Embed a word

        :returns: vector, or None if the word is outside of the vocabulary
        :rtype: ndarray
        """

        # Consider how you implement the vocab lookup.  It should be O(1).
        # convert words to dictionary for 0(1) lookup
        index = self.words.get(word, -1)
        if index != -1:
            return self.vecs[index]
        return

    @classmethod
    def from_files(cls, word_file, vec_file):
        """Instantiate an embedding from files

        Example::

            embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')

        :rtype: cls
        """
        return cls(load_words(word_file), load_vectors(vec_file))

    def embed_document(self, text):
        """Convert text to vector, by finding vectors for each word and combining

        :param str document: the document (one or more words) to get a vector
            representation for

        :return: vector representation of document
        :rtype: ndarray (1D)
        """
        # Use tokenize(), maybe map(), functools.reduce, itertools.aggregate...
        # Assume any words not in the vocabulary are treated as 0's
        # Return a zero vector even if no words in the document are part
        # of the vocabulary
        # parse the text
        wordtokens = tokenize(self, text)
        # call the constructor using lambda to get vector on these tokens/word
        # store vector in a list
        wordlist = list(filter(None.__ne__, map(lambda x: self(x), wordtokens)))
        # convert the list to numpy array
        wordvec = np.array(wordlist)
        # get the sum of all words of numpy array
        if wordvec.size > 0:
            sumvec = wordvec.sum(axis=0)
            return sumvec
        # return zero vector in case word is not found
        return np.zeros(self.vecs.shape[1])


def tokenize(self, text):
    # Get all "words", including contractions
    # eg tokenize("Hello, I'm Scott") --> ['hello', "i'm", 'scott']
    return re.findall(r"\w[\w']+", text.lower())





def cosine_similarity(a, b):
    """This function compute cosine similarity between two vectors a and b
    :param numpy.array a ->  first vector
    :param numpy.array b -> second vector which will be compared with first
    :returns: cosine distance if both vector is non empty else nan
    :rtype: float or nan
    """
    if (np.count_nonzero(a)) and (np.count_nonzero(b)):
        return (np.dot(a, b)) / (np.linalg.norm(a) * np.linalg.norm(b))
    else:
        return np.nan

def cosine_distance (a,b):
    return 1 - cosine_similarity (a,b)

def delete_files(*args):
    """ This function deletes files from testdata folder if exists"""
    for filename in args:
        if os.path.isfile(filename):
            os.remove(filename)