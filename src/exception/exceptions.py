class CliException(Exception):
    """
    Base CLI Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = "An unknown exception occurred"

    def __init__(self, *args, **kwargs):
        try:
            self._error_string = self.message % kwargs
        except Exception:
            # at least get the core message out if something happened
            self._error_string = self.message
        if len(args) > 0:
            # If there is a non-kwarg parameter, assume it's the error
            # message or reason description and tack it on to the end
            # of the exception message
            # Convert all arguments into their string representations...
            args = ["%s" % arg for arg in args]
            self._error_string = (self._error_string +
                                 "\nDetails: %s" % '\n'.join(args))

    def __str__(self):
        return self._error_string


class InvalidConfiguration(CliException):
    message = "Invalid Configuration"


class NotFound(CliException):
    message = "Object not found"


class Unauthorized(CliException):
    message = 'Unauthorized'


class TimeoutException(CliException):
    message = "Request timed out"


class BuildErrorException(CliException):
    message = "Server %(server_id)s failed to build and is in ERROR status"


class AddImageException(CliException):
    message = "Image %(image_id) failed to become ACTIVE in the allotted time"


class VolumeBuildErrorException(CliException):
    message = "Volume %(volume_id)s failed to build and is in ERROR status"


class BadRequest(CliException):
    message = "Bad request"


class AuthenticationFailure(CliException):
    message = ("Authentication with user %(user)s and password "
               "%(password)s failed")


class EndpointNotFound(CliException):
    message = "Endpoint not found"


class RateLimitExceeded(CliException):
    message = ("Rate limit exceeded.\nMessage: %(message)s\n"
               "Details: %(details)s")


class OverLimit(CliException):
    message = "Quota exceeded"


class ComputeFault(CliException):
    message = "Got compute fault"


class IdentityError(CliException):
    message = "Got identity error"


class Duplicate(CliException):
    message = "An object with that identifier already exists"


class SSHTimeout(CliException):
    message = ("Connection to the %(host)s via SSH timed out.\n"
               "User: %(user)s, Password: %(password)s")


class SSHExecCommandFailed(CliException):
    ''' Raised when remotely executed command returns nonzero status.  '''
    message = ("Command '%(command)s', exit status: %(exit_status)d, "
               "Error:\n%(strerror)s")


class ServerUnreachable(CliException):
    message = "The server is not reachable via the configured network"


class SQLException(CliException):
    message = "SQL error: %(message)s"


class DNSException(CliException):
    message = "DNS Client error: %(message)s"


class HwConfigException(CliException):
    message = "Hw-Config error: %(message)s"

class HaDbException(CliException):
    message = "HA error: %(message)s"
