import os
from datetime import datetime

from string import Template
from typing import Any, AnyStr, List

from attrs import define, field
from pydantic import DirectoryPath, FilePath, HttpUrl


def str2list(value: str):
    if isinstance(value, str):
        return [x.strip() for x in value.split(',')]
    else:
        type(value)
        print(value)
    return value

@define
class Post:
    title: AnyStr = field(metadata={"question": Template("What is the title of this post? ")})
    categories: List = field(
        converter=str2list,
        metadata={"question": Template("Provide a list of categories for this post: ")}
    )
    tags: List = field(
        converter=str2list,
        metadata={"question": Template("Provide a list of tags for this post: ")}
    )
    author: AnyStr = field(metadata={"question": Template("Who is the author of this post? ")})

    date: AnyStr = field(
        default=None,
        metadata={"question": Template(f"What date should this post be published? ")}
    )
    file_name: FilePath = field(factory=str)
    images: List[FilePath] = field(factory=list)

    def __attrs_post_init__(self):
        # if self.categories:
        #     if not isinstance(self.categories, list):
        #         try:
        #             self.categories = [x.strip() for x in self.categories.split(',')]
        #         except TypeError as te:
        #             # the provided value is not a list so we will just force it to a list
        #             self.categories = [self.categories]
        # if self.tags:
        #     try:
        #         self.tags = [x.strip() for x in self.tags.split(',')]
        #     except TypeError as te:
        #         # the provided value is not a list so we will just force it to a list
        #         self.tags = [self.tags]
        if not self.date:
            self.date = str(datetime.now())


@define
class Blog:
    title: AnyStr = field(metadata={"question": Template("What is the title of your blog? ")})
    author: AnyStr = field(metadata={"question": Template("What is the authors name? ")})
    github_username: AnyStr = field(metadata={"question": Template("What is your GitHub username? ")})

    theme: AnyStr = field(default="furo", metadata={"question": Template("Which theme do you want to use? ")})
    cname: AnyStr = field(
        default=None, 
        metadata={"question": Template("Please provide a CNAME if needed. If not then leave blank. ")}
    )
    posts: List[Post] = field(factory=list)

    directory: DirectoryPath = field(
        default='./blog', 
        metadata={"question": Template(f"Where should content be saved to? (default is ./blog/ ")}
    )

    def __attrs_post_init__(self):
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
