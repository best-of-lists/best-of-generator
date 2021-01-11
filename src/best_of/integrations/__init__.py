from typing import List

from best_of.integrations import (
    base_integration,
    conda_integration,
    dockerhub_integration,
    maven_integration,
    npm_integration,
    pypi_integration,
)

# libio and github integrations are a bit special

AVAILABLE_PACKAGE_MANAGER: List[base_integration.BaseIntegration] = [
    pypi_integration.PypiIntegration(),
    conda_integration.CondaIntegration(),
    npm_integration.NpmIntegration(),
    maven_integration.MavenIntegration(),
    dockerhub_integration.DockerhubIntegration(),
]

# TODO: "helm_id", "brew_id", "apt_id", "yum_id", "snap_id", "cargo_id", "maven_id", "dnf_id", "yay_id",
