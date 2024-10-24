import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmRHELPostgresqlImageStreams:

    def setup_method(self):
        package_name = "postgresql-imagestreams"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("10-el8", "registry.redhat.io/rhel8/postgresql-10:latest", False),
            ("13-el8", "registry.redhat.io/rhel8/postgresql-13:latest", True),
            ("13-el9", "registry.redhat.io/rhel9/postgresql-13:latest", True),
            ("15-el8", "registry.redhat.io/rhel8/postgresql-15:latest", True),
            ("15-el9", "registry.redhat.io/rhel9/postgresql-15:latest", True),
            ("16-el8", "registry.redhat.io/rhel8/postgresql-16:latest", True),
            ("16-el9", "registry.redhat.io/rhel9/postgresql-16:latest", True),
        ],
    )
    def test_package_imagestream(self, version, registry, expected):
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry) == expected
