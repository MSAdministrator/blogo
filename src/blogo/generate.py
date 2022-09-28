# Copyright: (c) 2022, MSAdministrator <rickardja@live.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from attr import asdict
from .base import Base
from .helper import Helper


class Generate(Base):
    """Used to generate blog content."""

    @property
    def deploy(self):
        """Used to deploy generated blog content."""
        raise NotImplementedError("Deploy is currently not implemented.")

    def now(self, directory: str = None):
        """Runs generation of blogo content."""
        
        Helper.install_package(package=self._blog.theme)
        if not directory:
            directory = self._create_folder(name=self._blog.github_pages_directory)
        for file in [".readthedocs.yml","mkdocs.yml"]:
            self.TEMPLATE_ENV.get_template(file).stream(asdict(self._blog)).dump(f"{directory}/{file}")
        directory = self._create_folder(
            name=f"{self._blog.github_pages_directory}/docs"
        )
        for file in ["conf.py","requirements.txt","index.md"]:
            self.TEMPLATE_ENV.get_template(file).stream(asdict(self._blog)).dump(f"{directory}/{file}")
