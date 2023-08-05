from drb import DrbNode
from drb.factory import DrbFactory, DrbSignature, DrbSignatureType


class ZipFactory(DrbFactory):
    def _create(self, node: DrbNode) -> DrbNode:
        return node


class ZipSignature(DrbSignature):
    def __init__(self):
        self._factory = ZipFactory()

    @property
    def uuid(self) -> str:
        return '53794b50-2778-11ec-9621-0242ac130002'

    @property
    def label(self) -> str:
        return 'zip'

    @property
    def category(self) -> DrbSignatureType:
        return DrbSignatureType.CONTAINER

    @property
    def factory(self) -> DrbFactory:
        return self._factory

    def match(self, node: DrbNode) -> bool:
        return node.name.lower().endswith('.zip')
