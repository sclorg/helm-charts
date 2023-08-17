import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmRHELPostgresqlImageStreams:

    def setup_method(self):
        package_name = "postgresql-imagestreams"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("13-el8", "registry.redhat.io/rhel8/postgresql-13:latest"),
            ("13-el9", "registry.redhat.io/rhel9/postgresql-13:latest"),
            ("10", "registry.redhat.io/rhscl/postgresql-10-rhel7:latest"),
            ("10-el7", "registry.redhat.io/rhscl/postgresql-10-rhel7:latest"),
            ("10-el8", "registry.redhat.io/rhel8/postgresql-10:latest"),
            ("12-el7", "registry.redhat.io/rhscl/postgresql-12-rhel7:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        self.hc_api.set_version("0.0.1")
        self.hc_api.helm_package()
        self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)


class TestHelmCentOSLPostgresqlImageStreams:

    def setup_method(self):
        package_name = "postgresql-imagestreams"
        path = test_dir / "../charts/centos"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("15-el9", "quay.io/sclorg/postgresql-15-c9s:latest"),
            ("13-el9", "quay.io/sclorg/postgresql-13-c9s:latest"),
            ("15-el8", "quay.io/sclorg/postgresql-15-c8s:latest"),
            ("13-el8", "quay.io/sclorg/postgresql-13-c8s:latest"),
            ("12-el8", "quay.io/sclorg/postgresql-12-c8s:latest"),
            ("10-el8", "quay.io/sclorg/postgresql-10-c8s:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        self.hc_api.set_version("0.0.1")
        self.hc_api.helm_package()
        self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)
