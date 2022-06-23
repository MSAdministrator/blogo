import json
import os
from glob import glob


import yaml
from attrs import asdict, has
from pick import pick
from jinja2 import Environment, PackageLoader, select_autoescape
from prompt_toolkit import PromptSession

from .utils.logger import LoggingBase


class Base(metaclass=LoggingBase):

    FILE_REPLACEMENT_CHARS = "!#$%^&*()_+ "
    session = PromptSession()
    __conf_path = None
    _blog = None
    count = 1
    TEMPLATE_ENV = Environment(
        loader=PackageLoader("blogo"),
        trim_blocks=True,
        lstrip_blocks=True
      #  autoescape=True
    )

    def __init__(self) -> None:
        blog = self.get_blog_conf_from_disk()
        if blog:
            from .models import Blog

            self._blog = Blog(**blog)

    def _prompt_options(self, title, options):
        options, index = pick(options, title)
        return options

    def _write_to_disk(self, name, data):
        with open(self.get_abs_path(name), "w+") as f:
            if has(data):
                yaml.dump(asdict(data), f)
            else:
                yaml.dump(data, f)
        return self.get_abs_path(name)

    def _save_to_disk(self, name, data):
        if not os.path.exists(self.get_abs_path(name)):
            return self._write_to_disk(name=name, data=data)
        else:
            self.count += 1
            return self._save_to_disk(f"{name.split('.yml')[0]}_{self.count}.yml", data)

    def _read_from_disk(self, path):
        if os.path.exists(self.get_abs_path(path)) and os.path.isfile(self.get_abs_path(path)):
            if path.endswith('.yml'):
                with open(self.get_abs_path(path)) as f:
                    return yaml.safe_load(f)
            elif path.endswith('.json'):
                with open(self.get_abs_path(path)) as f:
                    return json.load(f)

    def _search_disk(self, name):
        for item in glob(name):
            # we currently only return the first one found
            return item

    def get_abs_path(self, value) -> str:
        """Formats and returns the absolute path for a path value

        Args:
            value (str): A path string in many different accepted formats

        Returns:
            str: The absolute path of the provided string
        """
        return os.path.abspath(os.path.expanduser(os.path.expandvars(value)))

    def update_blog_conf_on_disk(self):
        self._write_to_disk(self.__conf_path, self._blog)
        self.__logger.info(f"Updated your blogo conf on disk.")

    def save_blog_conf_to_disk(self):
        return self._save_to_disk('.blogo.yml', self._blog)
    
    def get_blog_conf_from_disk(self):
        conf_found = self._search_disk(".blogo*.yml")
        if conf_found:
            self.__conf_path = conf_found
            return self._read_from_disk(conf_found)

    def save_post_template_to_disk(self, post):
        for char in self.FILE_REPLACEMENT_CHARS:
            post.title = post.title.replace(char, '-')
        if not os.path.exists(self._blog.directory):
            os.makedirs(self._blog.directory)
        template = self.TEMPLATE_ENV.get_template("post.md")
        post.file_name = self.get_abs_path(f"{self._blog.directory}/{post.title}.md")
        template.stream(**asdict(post)).dump(post.file_name)
