import time

import openai
from openai import OpenAI, BadRequestError
from read_email import get_new_email
import json

client = OpenAI()


def batch_email_parse(batch_size: int):
    messages = get_new_email()
    start = 0
    end = batch_size
    batch = messages[start:end]
    while len(batch) > 0:
        parse_email_receipts(batch)
        time.sleep(15.0)
        start = end if end <= len(messages) - 1 else None
        end = end + batch_size if end + batch_size <= len(messages) else len(messages)
        if start is not None:
            batch = messages[start:end]
        else:
            batch = []


def parse_email_receipts(messages: list[json]):
    # messages = get_new_email()
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant skilled in reading json blobs of recent emails. Given an array " +
                    "of JSON blobs representing emails your task is to determine " +
                    "whether it is a receipt. For each JSON blob in the array, please create an object with two fields: a " +
                    "boolean 'isReceipt' and a string 'vendor' with the vendor's name. Return an array of these JSON objects."
                },
                {
                    "role": "user",
                    "content": json.dumps(messages)
                }
            ]
        )
        print(completion.choices[0].message)
    except BadRequestError:
        print(f'bad request error for message:')
        return


def test():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
    )

    print(completion.choices[0].message)


if __name__ == '__main__':
    # parse_email_receipts()
    batch_email_parse(1)
    # models_data = openai.models.list().data
    # internal = [x for x in models_data if x.owned_by == 'openai-internal']
    # print(internal)
