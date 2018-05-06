import argparse
import re
import collections
import pymorphy2
import pandas as pd

from habr_parser import get_data


def get_nouns(text, morph=pymorphy2.MorphAnalyzer()):
    """
    Returns a string with all russian nouns and any words written
    in Latin alphabet from a given text string
    """
    lower_letters_regex = re.compile('[^a-zа-я]')
    words_string = text.lower().strip()
    words = lower_letters_regex.sub(
        ' ',
        words_string
    ).split()
    nouns = []
    for word in words:
        if ord(word[0]) < 128:  # checks if a word starts with latin symbols
            nouns.append(word)
            continue
        p = morph.parse(word)[0]
        if p.tag.POS == 'NOUN':
            nouns.append(p.normal_form)
    string_of_nouns = ' '.join(nouns)
    return string_of_nouns


def parse_titles(dataframe):
    """Replaces an article title in a dataframe with normalized nouns"""

    return dataframe['title'].apply(get_nouns)


def get_weekly_nouns(series):
    """
    Downsamples a series to weekly values by combining nouns from each article
    within a week into a string
    """
    return series.resample('W').apply(lambda x: ' '.join(x))


def calculate_word_frequency(weekly_data):
    """Defines the three most common words for each row in a series"""
    def get_three_most_common(text):
        words = text.split()
        three_most_common = collections.Counter(words).most_common(3)
        output = ' '.join([word for word, _ in three_most_common])
        return output
    return weekly_data.apply(get_three_most_common)


def collect_most_frequent_words(pages=10):
    data = get_data(pages=pages)
    data_parsed = parse_titles(data)
    weekly_data = get_weekly_nouns(data_parsed)
    output = calculate_word_frequency(weekly_data)
    return output


def print_most_frequent_words(series, ascending=True):
    dataframe = series.to_frame(name='title')
    dataframe.reset_index(inplace=True)
    new_column_names = {
        'date': 'End of the week',
        'title': 'The most frequent words'
    }
    dataframe.rename(columns=new_column_names, inplace=True)
    dataframe['Beginning of the week'] = (dataframe['End of the week']
                                          - pd.Timedelta('6 days'))
    dataframe = dataframe[['Beginning of the week',
                           'End of the week',
                           'The most frequent words']]
    if ascending is False:
        dataframe = dataframe.sort_index(ascending=False, axis=0)
    print(dataframe.to_string(index=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pages", type=int)
    args = parser.parse_args()
    if args.pages:
        pages = args.pages
    else:
        pages = 10
    result = collect_most_frequent_words(pages=pages)
    print_most_frequent_words(result, ascending=False)
