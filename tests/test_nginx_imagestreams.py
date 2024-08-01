import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmRHELNginxImageStreams:

    def setup_method(self):
        package_name = "nginx-imagestreams"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("1.24-ubi9", "registry.redhat.io/ubi9/nginx-124:latest"),
            ("1.24-ubi8", "registry.redhat.io/ubi8/nginx-124:latest"),
            ("1.22-ubi9", "registry.redhat.io/ubi9/nginx-122:latest"),
            ("1.22-ubi8", "registry.redhat.io/ubi8/nginx-122:latest"),
            ("1.20-ubi9", "registry.redhat.io/ubi9/nginx-120:latest"),
            ("1.20-ubi8", "registry.redhat.io/ubi8/nginx-120:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)


class TestHelmCentOSNginxImageStreams:

    def setup_method(self):
        package_name = "nginx-imagestreams"
        path = test_dir / "../charts/centos"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("1.24-ubi9", "registry.access.redhat.com/ubi9/nginx-124:latest"),
            ("1.24-ubi8", "registry.access.redhat.com/ubi8/nginx-124:latest"),
            ("1.22-ubi9", "registry.access.redhat.com/ubi9/nginx-122:latest"),
            ("1.22-ubi8", "registry.access.redhat.com/ubi8/nginx-122:latest"),
            ("1.20-ubi9", "registry.access.redhat.com/ubi9/nginx-120:latest"),
            ("1.20-ubi8", "registry.access.redhat.com/ubi8/nginx-120:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)
