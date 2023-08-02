import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmHttpdImageStreams:

    def setup_method(self):
        package_name = "php-imagestreams"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("latest", "registry.redhat.io/ubi8/php-80:latest"),
            ("8.0-ubi9", "registry.redhat.io/ubi9/php-80:latest"),
            ("8.0-ubi8", "registry.redhat.io/ubi8/php-80:latest"),
            ("7.4-ubi8", "registry.redhat.io/ubi8/php-74:latest"),
            ("7.3-ubi7", "registry.redhat.io/ubi7/php-73:latest"),
            ("7.3",  "registry.redhat.io/rhscl/php-73-rhel7:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        self.hc_api.set_version("0.0.1")
        self.hc_api.helm_package()
        self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)
