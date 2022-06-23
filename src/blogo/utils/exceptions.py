# Copyright: (c) 2022, MSAdministrator <rickardja@live.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)


class ConfigurationNotFoundError(FileNotFoundError):
    """Raised when a blogo configuration file was not found."""

    def __init__(self, message):
        """A provided message will be written to output.

        Args:
            message (str): A custom provided message.
        """
        super().__init__(message)


class FileExtensionNotSupportedError(Exception):
    """Raised when a file extension is not supported."""

    def __init__(self, message):
        """A provided message will be written to output.

        Args:
            message (str): A custom provided message.
        """
        super().__init__(message)


class IncorrectParametersError(Exception):
    """Raised when the incorrect configuration of parameters is passed into a Class."""

    pass


class MissingDefinitionFileError(Exception):
    """Raised when a definition file cannot be find."""

    pass


class MalformedFileError(Exception):
    """Raised when a file does not meet an expected and defined format structure."""

    pass
