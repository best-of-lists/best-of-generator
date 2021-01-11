from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import List

from addict import Dict


class BaseGenerator(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of the generator."""
        return NotImplemented

    @abstractmethod
    def write_output(
        self, categories: OrderedDict, projects: List[Dict], config: Dict, labels: list
    ) -> None:
        """Generates the markdown output and writes into files.

        Args:
            categories (OrderedDict): Projects categorized into configured categories.
            projects (list): List of projects.
            config (Dict): Best-of configuration.
            labels (list): List of avaialable labels.
        """
        pass
