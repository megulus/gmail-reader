import time

import openai
from openai import OpenAI, BadRequestError
from read_email import get_new_email
import json

client = OpenAI()


def batch_email_parse(batch_size: int) -> list[json]:
    all_output = []
    messages = get_new_email()
    print(f'number of messages: {len(messages)}')
    start = 0
    end = batch_size
    batch = messages[start:end]
    while len(batch) > 0:
        output = parse_email_receipts(batch)
        [all_output.append(json.dumps(x)) for x in output]
        start = end if end <= len(messages) - 1 else None
        end = end + batch_size if end + batch_size <= len(messages) else len(messages)
        if start is not None:
            batch = messages[start:end]
        else:
            batch = []
    return all_output


def parse_email_receipts(messages: list[json]) -> list[str]:
    output = []
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Given an array of JSON blobs representing emails your task is to determine " +
                               "1) whether it is a receipt, and 2) if yes, whether it is a receipt from Amazon. " +
                               "For each Amazon receipt that you find, create a JSON blob with the fields " +
                               "'date,' 'total,' 'order_number' and 'order_link' - the total should be the overall " +
                               "purchase total. The 'order_link' field should be a link to the order. For regular " +
                               "Amazon orders, use this format: " +
                               "`https://www.amazon.com/gp/your-account/order-details?ie=UTF8&orderID={order_number}`." +
                               "For digital orders (order numbers starting with D) use this format: " +
                               "`https://www.amazon.com/gp/digital/your-account/order-summary.html?ie=UTF8&orderID={order_number}`"
                               "Return all the JSON blobs created - one for each Amazon receipt - in an array." +
                               "Return an empty array if no Amazon receipts are found."
                },
                {
                    "role": "user",
                    "content": json.dumps(messages)
                }
            ]
        )
        output.append(completion.choices[0].message.content)
    except BadRequestError:
        print(f'bad request error')
    return output


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
    emails = batch_email_parse(5)
    for item in emails:
        j = json.loads(item)
        print(f'item type: {type(j)} item: {j}')
    # models_data = openai.models.list().data
    # internal = [x for x in models_data if x.owned_by == 'openai-internal']
    # print(internal)
