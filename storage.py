import os
import json

CONVERSATION_FILE = 'conversation_history.json'

def initialize_conversation():
    if not os.path.exists(CONVERSATION_FILE):
        with open(CONVERSATION_FILE, 'w') as file:
            json.dump([], file)

def save_message(role, message):
    initialize_conversation()
    with open(CONVERSATION_FILE, 'r') as file:
        conversation = json.load(file)

    conversation.append({"role": role, "content": message})

    with open(CONVERSATION_FILE, 'w') as file:
        json.dump(conversation, file, indent=4)

def get_conversation():
    initialize_conversation()
    with open(CONVERSATION_FILE, 'r') as file:
        conversation = json.load(file)
    return conversation

def clear_conversation():
    if os.path.exists(CONVERSATION_FILE):
        os.remove(CONVERSATION_FILE)