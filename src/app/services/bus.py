class CommandBus:
    def __init__(self):
        self.handlers = {}

    def register(self, command, handler):
        command_name = command.__name__
        self.handlers[command_name] = handler

    def execute(self, command):
        command_name = command.__class__.__name__
        if command_name not in self.handlers:
            raise ValueError(f"No handler for {command_name}")
        handler = self.handlers[command_name]
        return handler.execute(command)
