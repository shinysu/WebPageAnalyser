from bs4.element import Comment
from string import punctuation


def clean_string(inp_str):
    st = str.maketrans('', '', punctuation)
    return inp_str.translate(st).lower().strip().split()


def remove_stop_words(inp_dict):
    '''clean the dictionary of words by removing the stop words'''
    stop_word_list = get_stop_words()
    for word in stop_word_list:
        if word in inp_dict.keys():
            del inp_dict[word]
    return inp_dict


def get_stop_words():
    '''read stop words from the file into a list'''
    stop_word_list = []
    with open('stopwords.txt','r') as file:
        for word in file:
            stop_word_list.append(word.strip('\n'))
    return stop_word_list


def get_word_count(inp_str):
    st = clean_string(inp_str)
    d = {}
    total_count = len(st)
    for word in st:
        d[word] = d.get(word, 0) + 1
    unique_count = len(d.items())
    cleaned_d = remove_stop_words(d)
    sorted_d = dict(sorted(cleaned_d.items(), key=lambda kv:kv[1], reverse=True))
    return total_count, unique_count, list(sorted_d.keys())[:5]


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'meta', '[document]','noscript','header', 'html', 'input']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(soup):
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


