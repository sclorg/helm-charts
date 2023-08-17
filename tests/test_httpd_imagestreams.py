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

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("2.4-ubi9", "registry.redhat.io/ubi9/httpd-24:latest"),
            ("2.4-ubi8", "registry.redhat.io/ubi8/httpd-24:latest"),
            ("2.4-el8", "registry.redhat.io/rhel8/httpd-24"),
            ("2.4-el7", "registry.redhat.io/rhscl/httpd-24-rhel7"),
            ("2.4", "registry.redhat.io/rhscl/httpd-24-rhel7"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        self.hc_api.set_version("0.0.1")
        self.hc_api.helm_package()
        self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)


class TestHelmCentOSHttpdImagestreams:
    def setup_method(self):
        package_name = "httpd-imagestreams"
        path = test_dir / "../charts/centos"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)
    
    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry", 
        [
            ("2.4-ubi9", "registry.access.redhat.com/ubi9/httpd-24:latest"),
            ("2.4-ubi8", "registry.access.redhat.com/ubi8/httpd-24:latest"),
            ("2.4-el8", "docker.io/centos/httpd-24-centos8:latest"),
            ("2.4-el7", "quay.io/centos7/httpd-24-centos7:latest"),
            ("2.4", "quay.io/centos7/httpd-24-centos7:latest"),
        ]
    )
    def test_package_imagestream(self, version, registry):
        self.hc_api.set_version("0.0.1")
        self.hc_api.helm_package()
        self.hc_api.helm_installation()
        self.hc_api.check_imagestreams(version=version, registry=registry)
