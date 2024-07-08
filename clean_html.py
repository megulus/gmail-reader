import re
from bs4 import BeautifulSoup


def condense_newline(text):
    return '\n'.join([p for p in re.split('\n|\r|\t', text) if len(p) > 0])


def remove_non_text_chars(text):
    text = text.replace(u'\xa0', u' ')
    text = text.replace(u'\u2022', u' ')
    text = text.replace(u'\u2019', u"'")
    text = text.replace(u'\u21e2', u' ')
    text = re.sub(r'[&,!?+=<>\-\n\r\t\s]{2,}', ' ', text)
    return re.sub(r'\s{2,}', ' ', text)


def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    return soup.get_text()


if __name__=='__main__':
    with open('test_email_body.txt') as silly_string:
        text = silly_string.read()
        t2 = remove_non_text_chars(text)
        print(f'removed non-text chars: {t2}')

# from boilerpy3 import extractors
#
#
# def condense_newline(text):
#     return '\n'.join([p for p in re.split('\n|\r', text) if len(p) > 0])
#
#
# def parse_html(text):
#     html_extractor = extractors.ArticleExtractor()
#     return condense_newline(html_extractor.get_marked_html(text))

