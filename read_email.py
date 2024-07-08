import json
import re

from simplegmail import Gmail
from simplegmail.query import construct_query

from clean_html import clean_html, remove_non_text_chars


def get_new_email() -> list[json]:
    gmail = Gmail()

    # query_params = {
    #     "newer_than": (8, "day"),
    #     "older_than": (4, "day"),
    #     "unread": True,
    # }

    query_params = {
        "newer_than": (45, "day"),
        "labels": ["Coding/reckonloid/training"]
    }

    messages = gmail.get_messages(query=construct_query(query_params))
    print(f'Number of messages: {len(messages)}')
    messages_json = []
    for message in messages:
        raw_html = message.html
        try:
            cleaned_html = clean_html(raw_html)
        except TypeError:
            print(f'failed to parse: {message.sender}: {message.subject}')
            continue
        condensed_html = remove_non_text_chars(cleaned_html)
        json_str = json.dumps(
            {'date': message.date, 'sender': message.sender, 'subject': message.subject, 'body': condensed_html},
            indent=2)
        messages_json.append(json_str)
        # message.mark_as_unread()
    return messages_json


def filter_by_sender(messages: list[json], filter: str) -> list[json]:
    return [m for m in messages if re.search(filter, json.loads(m)['sender'])]


if __name__ == '__main__':
    msgs = filter_by_sender(get_new_email(), 'Amazon.com')
    for m in msgs:
        # print(f'MESSAGE\n: {m}')
        j = json.loads(m)
        print(f'DATE: {j['date']}')
        print(f'SENDER: {j['sender']}')
        # print(f'BODY\n: {j['body']}')
        # body = j['body']
        # cleaned = clean_html(body)
        # condensed = remove_non_text_chars(cleaned)
