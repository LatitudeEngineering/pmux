class ComputationRequest(object):
    """Entity encapsulating computation to be executed.

    """
    def __init__(self, function_name_string, stdin_list, metadata_dict):
        self._fn = function_name_string
        self._in = stdin_list
        self._meta = metadata_dict

    @property
    def function_name(self):
        return self._fn

    @property
    def stdin(self):
        return tuple(self._in)

    @property
    def metadata(self):
        return self._meta


class ComputationResponse(object):
    """Entity encapsulating a function execution attempt.

    """
    def __init__(self, function_name_string, stdout_list, stderr_list, metadata_dict):
        self._fn = function_name_string
        self._out = stdout_list
        self._err = stderr_list
        self._meta = metadata_dict

    @property
    def function_name(self):
        return self._fn

    @property
    def stdout(self):
        return tuple(self._out)

    @property
    def stderr(self):
        return tuple(self._err)

    @property
    def metadata(self):
        return self._meta
