from conversation_manager import ConversationManager


conversation = ConversationManager(max_history=5)


conversation.add_message(
    "user",
    "Which category generated the highest revenue?"
)

conversation.add_message(
    "assistant",
    "The beleza_saude category generated the highest revenue."
)

conversation.add_message(
    "user",
    "What about the second highest?"
)


print("=== CONVERSATION HISTORY ===")

for message in conversation.get_history():
    print(f"{message['role']}: {message['content']}")