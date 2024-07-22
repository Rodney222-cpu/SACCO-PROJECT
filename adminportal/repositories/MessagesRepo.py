import json
import os

def getMessages(app):
    messages = {}
    messages_file = os.path.join(os.path.abspath('adminportal'), 'repositories', 'messages.json')
    with open(messages_file) as messages_file:
        messages = json.load(messages_file)
        return messages