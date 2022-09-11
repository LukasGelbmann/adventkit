"""A build backend that reads the package version from version control.

Other than that, this build backend works like `flit_core`.
"""

__all__ = [
    "build_editable",
    "build_sdist",
    "build_wheel",
    "get_requires_for_build_editable",
    "get_requires_for_build_sdist",
    "get_requires_for_build_wheel",
    "prepare_metadata_for_build_editable",
    "prepare_metadata_for_build_wheel",
]

import contextlib

import flit_core.buildapi
import setuptools_scm
from flit_core.buildapi import (
    build_editable,
    get_requires_for_build_editable,
    get_requires_for_build_sdist,
    get_requires_for_build_wheel,
    prepare_metadata_for_build_editable,
    prepare_metadata_for_build_wheel,
)


def build_sdist(*args, **kwargs):
    """Build a source distribution, determining the version from metadata.

    The package version is derived from a tag on a commit in the version
    control system.
    """

    with override_version_file():
        return flit_core.buildapi.build_sdist(*args, **kwargs)


def build_wheel(*args, **kwargs):
    """Build a wheel, determining the version from metadata.

    If the wheel is built from a version-controlled repository, the package
    version is derived from a tag on a commit in the version control system.
    If, on the other hand, the wheel is built from a source distribution,
    the version is read from the `PKG-INFO` file.
    """

    with override_version_file():
        return flit_core.buildapi.build_wheel(*args, **kwargs)


@contextlib.contextmanager
def override_version_file():
    """Temporarily change the contents of the `_version.py` file."""

    version = setuptools_scm.get_version()
    temporary_content = (
        "# Generated file, not to be tracked in version control.\n"
        f"__version__ = {version!r}\n"
    )
    path = "src/adventkit/_version.py"
    with open(path, "r", encoding="utf-8") as file:
        original_content = file.read()

    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write(temporary_content)
        yield
    finally:
        with open(path, "w", encoding="utf-8") as file:
            file.write(original_content)
