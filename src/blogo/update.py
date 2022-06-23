from tkinter import *

from attrs import fields

from .base import Base
from .models import Post
from .editor import Editor
from .utils.exceptions import ConfigurationNotFound, IncorrectParameters




class Update(Base):

    @property
    def post(self):
        if not self._blog:
            raise ConfigurationNotFound("Unable to load your blogo configuration.")
        if not self._blog.posts:
            raise IncorrectParameters("There are not blog posts to update. Please create one first.")
        selected_post = self._prompt_options(
            title="Select post to update: ",
            options=[x.title for x in self._blog.posts]
        )
        blog_list = self._blog.posts
        for post in blog_list:
            if post.title == selected_post:
                self._blog.posts.remove(post)
                # _post = Post(
                #     title=self.session.prompt(fields(Post).title.metadata["question"].substitute()),
                #     categories=self.session.prompt(fields(Post).categories.metadata["question"].substitute()),
                #     tags=self.session.prompt(fields(Post).tags.metadata["question"].substitute()),
                #     author=self.session.prompt(fields(Post).author.metadata["question"].substitute()),
                #     date=self.session.prompt(fields(Post).date.metadata["question"].substitute())
                # )
                root = Tk()
                root.geometry("700x600")
                app = Editor(master=root, title=post.title, path=post.file_name, directory=self._blog.directory)
                app.mainloop()
                self._blog.posts.append(_post)
        path = self.save_post_template_to_disk(post=post)
        self.update_blog_conf_on_disk()
