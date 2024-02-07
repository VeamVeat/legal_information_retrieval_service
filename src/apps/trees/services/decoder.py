import json
from abc import ABC, abstractmethod
from xml.etree import ElementTree

from apps.trees.services.xml import XmlDictConfig


class BaseDecoder(ABC):
    @staticmethod
    @abstractmethod
    def decode(structure):
        ...


class XmlDecoder(BaseDecoder):
    @staticmethod
    def decode(structure) -> dict:
        tree = ElementTree.parse(structure)
        root = tree.getroot()
        return XmlDictConfig(root)


class JsonDecoder(BaseDecoder):
    @staticmethod
    def decode(structure):
        return json.loads(structure)
