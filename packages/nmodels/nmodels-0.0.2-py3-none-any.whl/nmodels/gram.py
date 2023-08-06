

def simple_unigram (string):
    """
    This function creates unigram from a string.

    :param string:
        The string as passed in by the user.

    :return:
        :rtype list
        A list of the unigrams
    """

    tokens = string.split()
    unigrams = list()

    # Creating bigrams via indexing
    for i in range(len(tokens)):
        unigrams.append([tokens[i]])

    return unigrams


def simple_bigram(string):
        """
        This function creates padded bigrams from the string passed in by the user.

        :param string:
            The string as passed in by the user.

        :return:
            :rtype list
            A list of the padded bigrams
        """

        # Simple tokens using white space
        tokens = string.split()
        bigrams = list()

        # Padding
        tokens.insert(0, "<START>")
        tokens[-1] = "<END>"

        # Creating bigrams via indexing
        for i in range(len(tokens)-1):
            bigrams.append((tokens[i], tokens[i+1]))

        return bigrams
