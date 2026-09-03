class ConversationManager:

    def __init__(self, max_history=5):
        self.history = []
        self.max_history = max_history

    def add_message(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })

        # Keep only the most recent messages
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []