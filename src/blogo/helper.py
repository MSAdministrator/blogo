from .base import Base


class Helper(Base):

    @classmethod
    def is_package_installed(cls, package):
        """Checks to see if package is installed.

        Args:
            package (str): The name of the package to check.

        Returns:
            bool: Returns true or false if installed.
        """
        import importlib.util

        spec = importlib.util.find_spec(package)
        if spec is None:
            return False
        return True

    @classmethod
    def install_package(cls, package, version=None):
        """Installs python packages.

        Args:
            package (str): The name of a python package.
            version (str, optional): The version of the python package. Defaults to None.
        """
        if not cls.is_package_installed(package=package):
            import pip

            if version:
                package = f"{package}=={version}"
            cls.__logger.info(f"Installing package {package}")

            if hasattr(pip, "main"):
                pip.main(["install", package])
                cls.__logger.info(f"Successfully installed package {package}")
                return True
            else:
                pip._internal.main(["install", package])
                cls.__logger.info(f"Successfully installed package {package}")
                return True
