from requests import Response


class SMSActivateRUError(Exception):
    pass


class Error(SMSActivateRUError):
    def __init__(self, req: Response) -> None:
        self.status_code = req.status_code
        self.text = req.text
        self.url = req.url
        Exception.__init__(self, f'code: {self.status_code} body: `{self.text}` url: {self.url}')


class NO_NUMBERS(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "There are no free numbers to receive SMS from the current service")


class NO_BALANCE(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "Out of balance")


class BAD_ACTION(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "Invalid action (action parameter)")


class BAD_SERVICE(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "Invalid service name (service parameter)")


class BAD_KEY(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "Invalid API access key")


class ERROR_SQL(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "One of the parameters has an invalid value")


class SQL_ERROR(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "One of the parameters has an invalid value")


class NO_ACTIVATION(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "The specified activation id does not exist")


class BAD_STATUS(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "Attempting to set a non-existent status")


class STATUS_CANCEL(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "Rent canceled with a refund")


class BANNED(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "Account is blocked")


class NO_CONNECTION(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "No connection to servers sms-activate")


class ACCOUNT_INACTIVE(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "No rooms available")


class NO_ID_RENT(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "No lease id specified")


class INVALID_PHONE(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "The room was not rented by you (wrong rental id)")


class STATUS_FINISH(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "Rent paid and completed")


class STATUS_WAIT_CODE(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "Waiting for the first SMS")


class INCORECT_STATUS(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "Missing or invalid status")


class CANT_CANCEL(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "Unable to cancel lease (more than 20 minutes passed)")


class ALREADY_FINISH(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "Lease has already ended")


class ALREADY_CANCEL(SMSActivateRUError):
    def __init__(self) -> None:
        Exception.__init__(self, "The lease has already been canceled")
