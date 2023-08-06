class BaseAuthCodeFlowError(Exception):
    pass


class AuthCodeFlowError(BaseAuthCodeFlowError):
    def __init__(self, response, *args, **kwargs):
        self.response = response
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"response={self.response}"
