from drb import DrbNode
from drb.factory import DrbFactory, DrbSignature, DrbSignatureType


class TextFactory(DrbFactory):
    def _create(self, node: DrbNode) -> DrbNode:
        return node


class ZipSignature(DrbSignature):
    def __init__(self):
        self._factory = TextFactory()

    @property
    def uuid(self) -> str:
        return '3d797648-281a-11ec-9621-0242ac130002'

    @property
    def label(self) -> str:
        return 'Text'

    @property
    def category(self) -> DrbSignatureType:
        return DrbSignatureType.FORMATTING

    @property
    def factory(self) -> DrbFactory:
        return self._factory

    def match(self, node: DrbNode) -> bool:
        return node.name.endswith('.txt')
