# Copyright: (c) 2022, MSAdministrator <rickardja@live.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

import json
import os
from glob import glob

import yaml
from attrs import asdict
from attrs import has
from jinja2 import Environment
from jinja2 import PackageLoader
from pick import pick
from prompt_toolkit import PromptSession

from .utils.exceptions import FileExtensionNotSupportedError
from .utils.logger import LoggingBase


class Base(metaclass=LoggingBase):
    """Base class for all blogo classes."""

    FILE_REPLACEMENT_CHARS = "!#$%^&*()_+ "
    session = PromptSession()
    __conf_path = None
    _blog = None
    count = 1
    TEMPLATE_ENV = Environment(loader=PackageLoader("blogo"), trim_blocks=True, lstrip_blocks=True, autoescape=True)

    def __init__(self) -> None:
        """Init ensures that blog configuration is loaded or not."""
        blog = self.get_blog_conf_from_disk()
        if blog:
            from .models import Blog

            self._blog = Blog(**blog)

    def _prompt_options(self, title: str, options: list) -> list:
        """Prompts user with list of options to select.

        Args:
            title (str): The title of the pick list prompt.
            options (list): A list of selection options.

        Returns:
            list: A list of selected options.
        """
        options, index = pick(options, title)
        return options

    def _create_folder(self, name):
        from .files import is_path_exists_or_creatable

        if is_path_exists_or_creatable(self.get_abs_path(name)):
            if not os.path.exists(self.get_abs_path(name)):
                os.makedirs(self.get_abs_path(name))
        return self.get_abs_path(name)

    def _write_to_disk(self, name, data):
        """Writes values to a local disk.

        Args:
            name (str): The name of the file path to write data to.
            data (dict or Attrs): The data to write.

        Returns:
            str: Returns path to the file on disk.
        """
        with open(self.get_abs_path(name), "w+") as f:
            if has(data):
                yaml.dump(asdict(data), f)
            else:
                yaml.dump(data, f)
        return self.get_abs_path(name)

    def _save_to_disk(self, name, data):
        """Used to save data to disk.

        This method ensures that files with existing names will be incremented accordingly.

        Args:
            name (str): The name of the file path to write to.
            data (dict or Attrs): The data to write to the provided file path.

        Returns:
            str: Returns path to the file on disk.
        """
        if not os.path.exists(self.get_abs_path(name)):
            return self._write_to_disk(name=name, data=data)
        else:
            self.count += 1
            return self._save_to_disk(f"{name.split('.yml')[0]}_{self.count}.yml", data)

    def _read_from_disk(self, path):
        """Reads yaml or json files from disk given a provided path.

        Args:
            path (str): A file ending in .yml or .json

        Raises:
            FileExtensionNotSupportedError: Raised when a path containing an unsupported extension is provided.

        Returns:
            dict: Returns a dictionary of the contents of a file.
        """
        if os.path.exists(self.get_abs_path(path)) and os.path.isfile(self.get_abs_path(path)):
            if path.endswith(".yml"):
                with open(self.get_abs_path(path)) as f:
                    return yaml.safe_load(f)
            elif path.endswith(".json"):
                with open(self.get_abs_path(path)) as f:
                    return json.load(f)
            else:
                raise FileExtensionNotSupportedError(f"The provided file is not supported: '{self.get_abs_path(path)}'")

    def _search_disk(self, pattern):
        """Searches disk for the first configuration file found.

        Args:
            pattern (str): The pattern of the file to search for.

        Returns:
            str: A file matching the provided pattern.
        """
        for item in glob(pattern):
            # we currently only return the first one found
            return item

    def get_abs_path(self, value) -> str:
        """Formats and returns the absolute path for a path value.

        Args:
            value (str): A path string in many different accepted formats

        Returns:
            str: The absolute path of the provided string
        """
        return os.path.abspath(os.path.expanduser(os.path.expandvars(value)))

    def update_blog_conf_on_disk(self):
        """Updates a blogo configuration file on disk."""
        self._write_to_disk(self.__conf_path, self._blog)
        self.__logger.info("Updated your blogo conf on disk.")

    def save_blog_conf_to_disk(self):
        """Saves a blogo configuration file on disk."""
        return self._save_to_disk(".blogo.yml", self._blog)

    def get_blog_conf_from_disk(self):
        """Retrieves a blogo configuration file on disk."""
        conf_found = self._search_disk(".blogo*.yml")
        if conf_found:
            self.__conf_path = conf_found
            return self._read_from_disk(conf_found)

    def save_post_template_to_disk(self, post):
        """Saves a blogo post component template to disk.

        Args:
            post (Post): A Post data model object.
        """
        for char in self.FILE_REPLACEMENT_CHARS:
            post.title = post.title.replace(char, "-")
        if not os.path.exists(self._blog.directory):
            os.makedirs(self._blog.directory)
        template = self.TEMPLATE_ENV.get_template("post.md")
        post.file_name = self.get_abs_path(f"{self._blog.directory}/{post.title}.md")
        template.stream(**asdict(post)).dump(post.file_name)
