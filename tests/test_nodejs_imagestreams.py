import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmRHELNodeJSImageStreams:

    def setup_method(self):
        package_name = "redhat-nodejs-imagestreams"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry",
        [
            ("22-ubi9", "registry.redhat.io/ubi9/nodejs-22:latest"),
            ("22-ubi9-minimal", "registry.redhat.io/ubi9/nodejs-22-minimal:latest"),
            ("20-ubi9", "registry.redhat.io/ubi9/nodejs-20:latest"),
            ("20-ubi9-minimal", "registry.redhat.io/ubi9/nodejs-20-minimal:latest"),
            ("20-ubi8", "registry.redhat.io/ubi8/nodejs-20:latest"),
            ("20-ubi8-minimal", "registry.redhat.io/ubi8/nodejs-20-minimal:latest"),
            ("18-ubi9", "registry.redhat.io/ubi9/nodejs-18:latest"),
            ("18-ubi9-minimal", "registry.redhat.io/ubi9/nodejs-18-minimal:latest"),
            ("18-ubi8", "registry.redhat.io/ubi8/nodejs-18:latest"),
            ("18-ubi8-minimal", "registry.redhat.io/ubi8/nodejs-18-minimal:latest"),
        ],
    )
    def test_package_imagestream(self, version, registry):
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        assert self.hc_api.check_imagestreams(version=version, registry=registry)
