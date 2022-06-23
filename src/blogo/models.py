# Copyright: (c) 2022, MSAdministrator <rickardja@live.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

import os
from datetime import datetime
from string import Template
from typing import AnyStr
from typing import List

from attrs import define
from attrs import field
from pydantic import DirectoryPath
from pydantic import FilePath


def str2list(value: str):
    """Used to convert strings to lists.

    Args:
        value (str): A string of values

    Returns:
        list: Returns a list of strings
    """
    if isinstance(value, str):
        return [x.strip() for x in value.split(",")]
    return value


@define
class Post:
    """A blogo post component data model."""

    title: AnyStr = field(metadata={"question": Template("What is the title of this post? ")})
    categories: List = field(
        converter=str2list, metadata={"question": Template("Provide a list of categories for this post: ")}
    )
    tags: List = field(converter=str2list, metadata={"question": Template("Provide a list of tags for this post: ")})
    author: AnyStr = field(metadata={"question": Template("Who is the author of this post? ")})

    date: AnyStr = field(default=None, metadata={"question": Template("What date should this post be published? ")})
    file_name: FilePath = field(factory=str)
    images: List[FilePath] = field(factory=list)

    def __attrs_post_init__(self):
        """Used to update default values."""
        if not self.date:
            self.date = str(datetime.now())


@define
class Blog:
    """A blogo blog data model.

    Raises:
        te: Raised when missing types for Post objects
    """

    title: AnyStr = field(metadata={"question": Template("What is the title of your blog? ")})
    author: AnyStr = field(metadata={"question": Template("What is the authors name? ")})
    github_username: AnyStr = field(metadata={"question": Template("What is your GitHub username? ")})

    theme: AnyStr = field(default="furo", metadata={"question": Template("Which theme do you want to use? ")})
    cname: AnyStr = field(
        default=None, metadata={"question": Template("Please provide a CNAME if needed. If not then leave blank. ")}
    )
    posts: List[Post] = field(factory=list)

    directory: DirectoryPath = field(
        default="./blog", metadata={"question": Template("Where should content be saved to? (default is ./blog/ ")}
    )

    def __attrs_post_init__(self):
        """Used to force object types."""
        if self.posts:
            return_list = []
            for post in self.posts:
                try:
                    return_list.append(Post(**post))
                except TypeError as te:
                    raise te
            self.posts = return_list
        if self.directory:
            self.directory = os.path.abspath(os.path.expanduser(os.path.expandvars(self.directory)))
