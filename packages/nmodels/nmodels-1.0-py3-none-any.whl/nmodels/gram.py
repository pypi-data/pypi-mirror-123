def simple_bigram(string):
    """
    This function creates padded bigrams from the string
    passed in by the user.

    :param string:
        The string as passed  in by the user.

    :return:
        :rtype list
        A list of the padded bigrams
    """

    # Simple tokens using white space
    tokens = string.split()

    # Padding
    tokens.insert(0, "<START>")
    tokens[-1] = "<END>"

    results = list()

    for i in range(len(tokens)-1):
        results.append((tokens[i], tokens[i+1]))

    return results
