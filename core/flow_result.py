class FlowResult:

    def __init__(self, success=True, data=None, message=""):
        self.success = success
        self.data = data or {}
        self.message = message

    def __repr__(self):
        return f"<FlowResult success={self.success} data={self.data} message={self.message}>"