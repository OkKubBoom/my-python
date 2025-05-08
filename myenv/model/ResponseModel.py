class ResponseModel:
    def __init__(self, status, success, message, data=None, error=None):
        self.status = status
        self.success = success
        self.message = message
        self.data = data
        self.error = error

    def to_dict(self):
        return {
            'status': self.status,
            'success': self.success,
            'message': self.message,
            'data': self.data,
            'error': self.error
        }
