"""
Checker focussing of completeness of feature files, e. g. that every scenario must have a name,
every parameter that is used in a scenario outline has to be defined in the examples, etc.
"""

from typing import Union

from gherlint.checkers.base_checker import BaseChecker
from gherlint.objectmodel import nodes
from gherlint.registry import CheckerRegistry
from gherlint.reporting import Message


class CompletenessChecker(BaseChecker):
    """Concerned about things like missing examples etc."""

    MESSAGES = [
        Message("W001", "missing-feature-name", "Feature has no name"),
        Message("W002", "missing-scenario-name", "Scenario has no name"),
    ]

    def visit_feature(self, node: nodes.Feature) -> None:
        if not node.name.strip():
            self.reporter.add_message("missing-feature-name", node)

    def visit_scenario(self, node: nodes.Scenario) -> None:
        self._check_missing_scenario_name(node)

    def visit_scenariooutline(self, node: nodes.ScenarioOutline) -> None:
        self._check_missing_scenario_name(node)

    def _check_missing_scenario_name(
        self, node: Union[nodes.Scenario, nodes.ScenarioOutline]
    ) -> None:
        if not node.name.strip():
            self.reporter.add_message("missing-scenario-name", node)


def register_checker(registry: CheckerRegistry) -> None:
    registry.register(CompletenessChecker)
