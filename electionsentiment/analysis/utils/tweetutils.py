import sys
import pickle
import random


def file_to_wordset(filename):
    ''' Converts a file with a word per line to a Python set '''
    words = []
    with open(filename, 'r') as f:
        for line in f:
            words.append(line.strip())
    return set(words)


def write_status(i, total):
    ''' Writes status of a process to console '''
    sys.stdout.write('\r')
    sys.stdout.write('Processing %d/%d' % (i, total))
    sys.stdout.flush()


def save_results_to_csv(results, csv_file):
    ''' Save list of type [(tweet_id, positive)] to csv in Kaggle format '''
    with open(csv_file, 'w') as csv:
        csv.write('id,prediction, polarity, subjectivity, compound, neg, neu, pos, a_count, v_count, d_count, affect_count, mood, tweet\n')
        for tweet_id, pred, nlpol, nlsub, compound, neg, neu, pos , ascore, vscore, dscore, affectscore, mood, tweet in results:
            csv.write(tweet_id)
            csv.write(',')
            csv.write(str(pred))
            csv.write(',')
            csv.write(str(nlpol))
            csv.write(',')
            csv.write(str(nlsub))
            csv.write(',')
            csv.write(str(compound))
            csv.write(',')
            csv.write(str(neg))
            csv.write(',')
            csv.write(str(neu))
            csv.write(',')
            csv.write(str(pos))
            csv.write(',')

            csv.write(str(ascore))
            csv.write(',')
            csv.write(str(vscore))
            csv.write(',')
            csv.write(str(dscore))
            csv.write(',')
            csv.write(str(affectscore))
            csv.write(',')
            csv.write(str(mood))
            csv.write(',')

            csv.write(str(tweet))
            csv.write(',')
            csv.write('\n')


def top_n_words(pkl_file_name, N, shift=0):
    """
    Returns a dictionary of form {word:rank} of top N words from a pickle
    file which has a nltk FreqDist object generated by stats.py

    Args:
        pkl_file_name (str): Name of pickle file
        N (int): The number of words to get
        shift: amount to shift the rank from 0.
    Returns:
        dict: Of form {word:rank}
    """
    with open(pkl_file_name, 'rb') as pkl_file:
        freq_dist = pickle.load(pkl_file)
    most_common = freq_dist.most_common(N)
    words = {p[0]: i + shift for i, p in enumerate(most_common)}
    return words


def top_n_bigrams(pkl_file_name, N, shift=0):
    """
    Returns a dictionary of form {bigram:rank} of top N bigrams from a pickle
    file which has a Counter object generated by stats.py

    Args:
        pkl_file_name (str): Name of pickle file
        N (int): The number of bigrams to get
        shift: amount to shift the rank from 0.
    Returns:
        dict: Of form {bigram:rank}
    """
    with open(pkl_file_name, 'rb') as pkl_file:
        freq_dist = pickle.load(pkl_file)
    most_common = freq_dist.most_common(N)
    bigrams = {p[0]: i for i, p in enumerate(most_common)}
    return bigrams


def split_data(tweets, validation_split=0.1):
    """Split the data into training and validation sets

    Args:
        tweets (list): list of tuples
        validation_split (float, optional): validation split %

    Returns:
        (list, list): training-set, validation-set
    """
    index = int((1 - validation_split) * len(tweets))
    random.shuffle(tweets)
    return tweets[:index], tweets[index:]
