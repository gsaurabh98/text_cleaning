# -*- coding: utf-8 -*-
"""
Created on Thus May 30 15:46:56 2019
Author: saurabh
"""

import re
import string

from contractions import contractions_dict
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from textblob import TextBlob


class Text:

    def __init__(self):
        pass

    def expand_contractions(self, text):
        """
        This function expand the given text eg: couldn't -> could not
        Parameters
        ----------
        text : str
                input string
        Returns
        -------
        str
            expanded string
        """

        pattern = re.compile(
            "({})".format("|".join(contractions_dict.keys())),
            flags=re.DOTALL | re.IGNORECASE)

        def replace_text(t):
            txt = t.group(0)
            if txt.lower() in contractions_dict.keys():
                return contractions_dict[txt.lower()]

        expand_text = pattern.sub(replace_text, text)
        return expand_text

    def remove_repeated_characters(self, word):
        """
        This function removes the repeated chars in a word
        Parameters
        ----------
        word : str
                input string
        Returns
        -------
        str
            clean words without repeating chars
        """

        pattern = re.compile(r"(\w*)(\w)\2(\w*)")
        substitution_pattern = r"\1\2\3"
        while True:
            if wordnet.synsets(word):
                return word
            new_word = pattern.sub(substitution_pattern, word)
            if new_word != word:
                word = new_word
                continue
            else:
                return new_word

    def cleaning(self, input_data, options):
        '''
        This function cleans the text as per the options selected by user

        Parameters
        ------------
        input_data: str
            input string to be cleaned
        options: list
            list of cleaning operations to be performed

        Returns
        ------------
        str
            Cleaned text
        '''

        # setting to lower
        input_data = input_data.lower()

        # Removing special chars
        if "Remove special characters" in options:
            input_data = input_data.replace('_', ' ')
            without_special_chars = re.sub("[^A-Za-z]", "", input_data)

        # Removing small words
        if "Remove words with length less than 3" in options:
            input_data = ' '.join(word for word in without_special_chars.split() \
                                  if len(word) > 3)

        # removing urls from text
        # http matches literal characters
        # \S+ matches all non-whitespace characters (the end of the url)
        # we replace with the empty string
        if "Remove hyperlinks" in options:
            input_data = re.sub(r"http\S+", "", input_data)

        # Fixes contractions such as `you're` to you `are`
        if "Expand contractions" in options:
            input_data = self._expand_contractions(input_data)

        # White spaces removal
        input_data = input_data.strip()

        # removing numbers
        if "Remove numbers" in options:
            input_data = re.sub(r'\d+', '', input_data)

        # Punctuation removal
        if "Remove punctuations" in options:
            input_data = input_data.translate(
                str.maketrans('', '', string.punctuation))

        # converting sentence into tokens
        tokens = word_tokenize(input_data)

        # removing repeated chars
        if "Remove repeated characters" in options:
            tokens = [self._remove_repeated_characters(s) for s in
                      tokens]

        # correcting the spelling of text
        if "Spelling correction" in options:
            tokens = [str(TextBlob(words).correct()) for words in
                      tokens]

        # # removing stop words
        stop_words = set(stopwords.words('english'))
        #
        nostopwods = [word for word in tokens if not word in stop_words]

        # morphological analysis of the words studies->study
        # Now just remove along with stemming words
        if "Perform lemmatization" in options:
            tokens = [lemmatizer.lemmatize(word) for word in
                      nostopwods]

        # keeping same order of text
        tokens = sorted(set(tokens), key=tokens.index)

        clean_text = ' '.join(tokens)

        return clean_text
