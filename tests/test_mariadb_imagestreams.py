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
            ("10.5-el9", "registry.redhat.io/rhel9/mariadb-105:latest"),
            ("10.3-el8", "registry.redhat.io/rhel8/mariadb-103:latest"),
            ("10.5-el8", "registry.redhat.io/rhel8/mariadb-105:latest"),
            ("10.3-el7", "registry.redhat.io/rhscl/mariadb-103-rhel7:latest"),
            ("10.3", "registry.redhat.io/rhscl/mariadb-103-rhel7:latest"),
            ("10.5-el7", "registry.redhat.io/rhscl/mariadb-105-rhel7:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        self.hc_api.set_version("0.0.1")
        self.hc_api.helm_package()
        self.hc_api.helm_installation()
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
            ("10.5-el7", "quay.io/centos7/mariadb-105-centos7:latest"),
            ("10.3-el8", "docker.io/centos/mariadb-103-centos8:latest"),
            ("10.3-el7", "quay.io/centos7/mariadb-103-centos7:latest"),
            ("10.3", "quay.io/centos7/mariadb-103-centos7:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        self.hc_api.set_version("0.0.1")
        self.hc_api.helm_package()
        self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)
