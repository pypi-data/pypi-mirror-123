from typing import Text, List

from cnside import metadata
from cnside.documents.base import Document
from cnside.objects.core import UnifiedPackageID

__all__ = ["CNSIDERequestDocument"]


class CNSIDERequestDocument(Document):
    def __init__(self, package_manager: Text, packages: List[UnifiedPackageID] = None, manifest: Text = None,
                 project: Text = 'abc'):
        super().__init__()
        if package_manager == metadata.packages.PackageManagers.PIP:
            self.package_manager = metadata.packages.PackageRepositories.PYPI
        else:
            self.package_manager = package_manager

        self.packages = packages
        self.manifest = manifest
        self.project = project
