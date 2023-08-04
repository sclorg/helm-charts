import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmPythonImageStreams:

    def setup_method(self):
        package_name = "python-imagestreams"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("3.11-ubi9", "registry.redhat.io/ubi9/python-311:latest"),
            ("3.11-ubi8", "registry.redhat.io/ubi8/python-311:latest"),
            ("3.9-ubi9", "registry.redhat.io/ubi9/python-39:latest"),
            ("3.9-ubi8", "registry.redhat.io/ubi8/python-39:latest"),
            ("3.8-ubi8", "registry.redhat.io/ubi8/python-38:latest"),
            ("3.8-ubi7", "registry.redhat.io/ubi7/python-38:latest"),
            ("3.8", "registry.redhat.io/rhscl/python-38-rhel7:latest"),
            ("3.6-ubi8", "registry.redhat.io/ubi8/python-36:latest"),
            ("2.7-ubi8", "registry.redhat.io/ubi8/python-27:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        self.hc_api.set_version("0.0.1")
        self.hc_api.helm_package()
        self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)
