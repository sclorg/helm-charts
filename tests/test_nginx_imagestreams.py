import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmMariadbImageStreams:

    def setup_method(self):
        package_name = "nginx-imagestreams"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("1.20-ubi9", "registry.redhat.io/ubi9/nginx-120:latest"),
            ("1.20-ubi8", "registry.redhat.io/ubi8/nginx-120:latest"),
            ("1.20-ubi7", "registry.redhat.io/ubi7/nginx-120:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        self.hc_api.set_version("0.0.1")
        self.hc_api.helm_package()
        self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)
