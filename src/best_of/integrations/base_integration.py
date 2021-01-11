from abc import ABC, abstractmethod

from addict import Dict


class BaseIntegration(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        return NotImplemented

    @abstractmethod
    def update_project_info(self, project_info: Dict) -> None:
        pass

    @abstractmethod
    def generate_md_details(self, project: Dict, configuration: Dict) -> str:
        return NotImplemented
