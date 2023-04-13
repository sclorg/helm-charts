import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmVarnishImageStreams:

    def setup_method(self):
        package_name = "varnish-imagestreams"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("6-el8", "registry.redhat.io/rhel8/varnish-6:latest"),
            ("6-el7", "registry.redhat.io/rhscl/varnish-6-rhel7:latest"),
            ("5-el8", "registry.redhat.io/rhel8/varnish-5:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        self.hc_api.set_version("0.0.1")
        self.hc_api.helm_package()
        self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)
