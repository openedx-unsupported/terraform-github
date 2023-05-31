from unittest.mock import MagicMock, call, patch

import pytest

from .repo_checks import EnsureLabels


@pytest.fixture
def maintenance_label():
    """
    Quickly make a basic label to return via the API.
    """
    maintenance_label = MagicMock()
    maintenance_label.name = "maintenance"
    maintenance_label.color = "ff9125"
    maintenance_label.description = (
        "Routine upkeep necessary for the health of the platform"
    )

    return maintenance_label


# Our list of expected labels, normally defined in labels.yaml.
labels_yaml = [
    {
        "name": "maintenance",
        "color": "ff9125",
        "description": "Routine upkeep necessary for the health of the platform",
    }
]


@patch.object(EnsureLabels, "labels", labels_yaml)
class TestEnsureLabels:
    def test_check_for_no_change(self, maintenance_label):
        api = MagicMock()
        api.issues.list_labels_for_repo.side_effect = [[maintenance_label], None]
        check_cls = EnsureLabels(api, "test_org", "test_repo")

        # Make sure that the check returns True, indicating that no changes need to be made.
        assert check_cls.check()[0]

    def test_addition(self, maintenance_label):
        api = MagicMock()
        api.issues.list_labels_for_repo.return_value = []
        check_cls = EnsureLabels(api, "test_org", "test_repo")

        # The check should be false because the maintenance label should be missing.
        assert check_cls.check()[0] == False

        check_cls.fix()
        assert api.issues.create_label.called

        call_args = api.issues.create_label.call_args
        expected_call = call(
            owner="test_org",
            repo="test_repo",
            name=maintenance_label.name,
            color=maintenance_label.color,
            description=maintenance_label.description,
        )
        assert call_args == expected_call
        assert not api.issues.update_label.called

    def test_update_label(self, maintenance_label):
        maintenance_label.name = ":+1: Ma.in-t 'e'n_a\"nce!\" :-1:"
        api = MagicMock()
        api.issues.list_labels_for_repo.side_effect = [[maintenance_label], None]

        check_cls = EnsureLabels(api, "test_org", "test_repo")

        assert check_cls.check()[0] == False
        check_cls.fix()

        call_args = api.issues.update_label.call_args
        expected_call = call(
            owner="test_org",
            repo="test_repo",
            name=maintenance_label.name,
            color=maintenance_label.color,
            new_name="maintenance",
            description=maintenance_label.description,
        )

        assert call_args == expected_call
        assert not api.issues.create_label.called
        assert api.issues.update_label.called
