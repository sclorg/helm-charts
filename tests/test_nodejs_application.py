import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmNodeJSApplication:

    def setup_method(self):
        package_name = "redhat-nodejs-application"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir, shared_cluster=True)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version",
        [
            "22-ubi10",
            "22-ubi10-minimal",
            "22-ubi9",
            "22-ubi9-minimal",
            "20-ubi9",
            "20-ubi9-minimal"
            "20-ubi8",
            "20-ubi8-minimal",
        ],
    )
    def test_by_helm_test(self, version):
        self.hc_api.package_name = "redhat-nodejs-imagestreams"
        self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-nodejs-application"
        assert self.hc_api.helm_package()
        pod_name = f"nodejs-ex-{version}".replace("-minimal", "")
        assert self.hc_api.helm_installation(
            values={
                "nodejs": version,
                "namespace": self.hc_api.namespace,
                "name": pod_name
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix=pod_name)
        assert self.hc_api.test_helm_chart(expected_str=["Node.js Crud Application"])
