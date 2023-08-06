from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Union

import yaml

try:
    from yaml import CDumper as dumper
    from yaml import CLoader as loader
except:
    from yaml import Dumper as dumper
    from yaml import Loader as loader


class Serializable(ABC):
    """Base class that represents a serializable item.

    Methods
    -------
    to_dict(self) -> dict
        Serializes the Serialiable item into a dictionary.
    to_yaml(self)
        Serializes the Serialiable item into a YAML.
    """

    def to_dict(self):
        """Serializes the Serialiable item into a dictionary."""
        return asdict(self)

    def to_yaml(self):
        """Serializes the Serialiable item into a YAML."""
        return yaml.dump(self.to_dict(), Dumper=dumper)

    def __repr__(self):
        return self.to_yaml()
