import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmRHELRedisImageStreams:

    def setup_method(self):
        package_name = "redis-imagestreams"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("6-el9", "registry.redhat.io/rhel9/redis-6:latest", True),
            ("6-el8", "registry.redhat.io/rhel8/redis-6:latest", True),
        ],
    )
    def test_package_imagestream(self, version, registry, expected):
        assert self.hc_api.check_imagestreams(version=version, registry=registry) == expected
