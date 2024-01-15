import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmRHELPerlImageStreams:

    def setup_method(self):
        package_name = "perl-imagestreams"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("5.32-ubi9", "registry.redhat.io/ubi9/perl-532:latest"),
            ("5.32-ubi8", "registry.redhat.io/ubi8/perl-532:latest"),
            ("5.30-el7", "registry.redhat.io/rhscl/perl-530-rhel7:latest"),
            ("5.30", "registry.redhat.io/rhscl/perl-530-rhel7:latest"),
            ("5.26-ubi8", "registry.redhat.io/ubi8/perl-526:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        self.hc_api.helm_package()
        self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)


class TestHelmCentOSPerlImageStreams:

    def setup_method(self):
        package_name = "perl-imagestreams"
        path = test_dir / "../charts/centos"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("5.32-ubi9", "registry.access.redhat.com/ubi9/perl-532:latest"),
            ("5.32-ubi8", "registry.access.redhat.com/ubi8/perl-532:latest"),
            ("5.30-el7", "quay.io/centos7/perl-530-centos7:latest"),
            ("5.30", "quay.io/centos7/perl-530-centos7:latest"),
            ("5.26-ubi8", "registry.access.redhat.com/ubi8/perl-526:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        self.hc_api.helm_package()
        self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)
