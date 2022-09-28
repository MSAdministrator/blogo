# Copyright: (c) 2022, MSAdministrator <rickardja@live.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from .base import Base


class Blogo(Base):
    """Main entry point for generating blogo content.

    Raises:
        NotImplementedError: Raised when a property has not been implemented yet.
    """

    @property
    def new(self):
        """Gives access to create new blogo content components."""
        from .new import New

        return New()

    @property
    def update(self):
        """Gives access to update existing blogo content components."""
        from .update import Update

        return Update()

    @property
    def generate(self):
        """Gives access to generate blogo content for GitHub pages."""
        from .generate import Generate

        return Generate().now
        raise NotImplementedError("Generate is currently not implemented")

    @property
    def deploy(self):
        """Deploys generated blogo content to GitHub pages."""
        raise NotImplementedError("Deploy is currently not implemented")
