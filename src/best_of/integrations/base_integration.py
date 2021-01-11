from abc import ABC, abstractmethod

from addict import Dict


class BaseIntegration(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of the integration."""
        return NotImplemented

    @abstractmethod
    def update_project_info(self, project_info: Dict) -> None:
        """Updates the project metadata by fetching information from the package manager.

        Args:
            project_info (Dict): Collected project metadata.
        """
        pass

    @abstractmethod
    def generate_md_details(self, project: Dict, configuration: Dict) -> str:
        """Generates markdown details for the given project.

        Args:
            project (Dict): Collected project metadata.
            configuration (Dict): Best-of configuration.

        Returns:
            str: Generated markdown.
        """
        return NotImplemented
