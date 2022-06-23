from .base import Base


class Blogo(Base):

    @property
    def new(self):
        from .new import New
        
        return New()

    @property
    def update(self):
        from .update import Update

        return Update()

    @property
    def generate(self):
        raise NotImplementedError("Generate is currently not implemented")

    @property
    def deploy(self):
        raise NotImplementedError("Deploy is currently not implemented")
