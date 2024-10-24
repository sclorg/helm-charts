import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmRHELHttpdImageStreams:

    def setup_method(self):
        package_name = "httpd-imagestreams"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("2.4-ubi9", "registry.redhat.io/ubi9/httpd-24:latest", True),
            ("2.4-ubi8", "registry.redhat.io/ubi8/httpd-24:latest", True),
            ("2.4-el8", "registry.redhat.io/rhel8/httpd-24", True),
            ("2.4-el9", "registry.redhat.io/rhel9/httpd-24", True),
        ],
    )
    def test_httpd_imagestream(self, version, registry, expected):
        assert self.hc_api.check_imagestreams(version=version, registry=registry) == expected
