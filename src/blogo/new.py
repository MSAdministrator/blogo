# Copyright: (c) 2022, MSAdministrator <rickardja@live.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from attrs import fields

from .base import Base
from .models import Blog
from .models import Post


class New(Base):
    """Creates new blogo components."""

    @property
    def blog(self):
        """Creates a new blogo configuration file."""
        if self._blog:
            continue_or_not = self.session.prompt(
                f"You already have a blog config for '{self._blog.title}'. " "Do you want to create a new blog? "
            )
            if not continue_or_not.lower().startswith("y"):
                return
        self._blog = Blog(
            title=self.session.prompt(fields(Blog).title.metadata["question"].substitute()),
            author=self.session.prompt(fields(Blog).author.metadata["question"].substitute()),
            github_username=self.session.prompt(fields(Blog).github_username.metadata["question"].substitute()),
            directory=self.session.prompt(fields(Blog).directory.metadata["question"].substitute()),
        )
        self.__logger.info(f"Your blogo configuration file is located at {self.save_blog_conf_to_disk()}")

    @property
    def post(self):
        """Creates a new blogo post component.

        Returns:
            str: Returns the path to the created blog content file.
        """
        self.blog
        post = Post(
            title=self.session.prompt(fields(Post).title.metadata["question"].substitute()),
            categories=self.session.prompt(fields(Post).categories.metadata["question"].substitute()),
            tags=self.session.prompt(fields(Post).tags.metadata["question"].substitute()),
            author=self.session.prompt(fields(Post).author.metadata["question"].substitute()),
            date=self.session.prompt(fields(Post).date.metadata["question"].substitute()),
        )
        path = self.save_post_template_to_disk(post=post)
        self._blog.posts.append(post)
        self.update_blog_conf_on_disk()
        return path
