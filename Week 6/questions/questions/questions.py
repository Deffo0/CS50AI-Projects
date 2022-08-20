import math
import os
import string
import nltk
import sys
nltk.download('stopwords')
from nltk.corpus import stopwords
FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files_map = {}
    for file in os.listdir(directory):

        fd = open(os.path.join(directory, file), "r", encoding="utf8")
        files_map[file] = fd.read()
        fd.close()
    return files_map


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    words = nltk.tokenize.word_tokenize(document)

    for word in words.copy():
        if word in stopwords.words("english"):
            words.remove(word)
        else:
            punc_group = True
            for ch in word:
                if ch not in string.punctuation:
                    punc_group = False
                    break
            if punc_group:
                words.remove(word)
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    freq_dict = {}
    idf_dict = {}
    for document in documents:
        for word in set(documents[document]):
            if word not in freq_dict:
                freq_dict[word] = 1
            else:
                freq_dict[word] += 1
    for word in freq_dict:
        idf_dict[word] = math.log(len(documents)/freq_dict[word])

    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf_scores = {}.fromkeys(files, 0)

    for word in query:
        if word in idfs.keys():
            for file in files:
                tf_idf_scores[file] += files[file].count(word) * idfs[word]

    top = sorted([file for file in files], key=lambda x: tf_idf_scores[x], reverse=True)

    return top[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores = {sentence: {"idf": 0, "freq": 0, "query_den": 0} for sentence in sentences}

    for sentence in sentences:
        for word in query:
            if word in sentences[sentence]:
                scores[sentence]["idf"] += idfs[word]
                scores[sentence]["freq"] += sentences[sentence].count(word)

        scores[sentence]["query_den"] = scores[sentence]["freq"] / len(sentences[sentence])
    top = sorted([sentence for sentence in sentences], key=lambda x: (scores[x]["idf"], scores[x]["query_den"]), reverse=True)
    return top[:n]

if __name__ == "__main__":
    main()
