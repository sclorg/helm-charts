import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmRHELMariadbImageStreams:

    def setup_method(self):
        package_name = "mariadb-imagestreams"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("10.11-el9", "registry.redhat.io/rhel9/mariadb-1011:latest"),
            ("10.11-el8", "registry.redhat.io/rhel8/mariadb-1011:latest"),
            ("10.5-el9", "registry.redhat.io/rhel9/mariadb-105:latest"),
            ("10.3-el8", "registry.redhat.io/rhel8/mariadb-103:latest"),
            ("10.5-el8", "registry.redhat.io/rhel8/mariadb-105:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)


class TestHelmCentOSMariadbImageStreams:

    def setup_method(self):
        package_name = "mariadb-imagestreams"
        path = test_dir / "../charts/centos"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("10.3-el8", "quay.io/sclorg/mariadb-103-c8s:latest"),
            ("10.5-el8", "quay.io/sclorg/mariadb-105-c8s:latest"),
            ("10.5-el9", "quay.io/sclorg/mariadb-105-c9s:latest"),
            ("10.11-el8", "quay.io/sclorg/mariadb-1011-c8s:latest"),
            ("10.11-el9", "quay.io/sclorg/mariadb-1011-c9s:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)
