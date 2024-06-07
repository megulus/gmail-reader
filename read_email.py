import json

from simplegmail import Gmail
from simplegmail.query import construct_query

def get_new_email() -> list[json]:
    gmail = Gmail()

    query_params = {
        "newer_than": (3, "day"),
        "unread": True,
    }

    messages = gmail.get_messages(query=construct_query(query_params))
    # print(f'Number of messages: {len(messages)}')
    messages_json = []
    for message in messages:
        json_str = json.dumps(
            {'date': message.date, 'sender': message.sender, 'subject': message.subject, 'body': message.plain}, indent=2)
        # print(json_str)
        messages_json.append(json_str)
        message.mark_as_unread()
    return messages_json

# if __name__ == '__main__':
#     gmail = Gmail()
#
#     query_params = {
#         "newer_than": (1, "day"),
#         "unread": True,
#     }
#
#     messages = gmail.get_messages(query=construct_query(query_params))
#     print(f'Number of messages: {len(messages)}')
#     for message in messages:
#         json_str = json.dumps(
#             {'date': message.date, 'sender': message.sender, 'subject': message.subject, 'body': message.html}, indent=2)
#         print(json_str)
#         message.mark_as_unread()
