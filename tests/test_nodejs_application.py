import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmNodeJSApplication:

    def setup_method(self):
        package_name = "nodejs-application"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version",
        [
            "20-ubi9",
            "20-ubi9-minimal"
            "20-ubi8",
            "20-ubi8-minimal",
            "18-ubi9",
            "18-ubi9-minimal",
            "18-ubi8",
            "18-ubi8-minimal",
        ],
    )
    def test_curl_connection(self, version):
        if self.hc_api.oc_api.shared_cluster:
            pytest.skip("Do NOT test on shared cluster")
        self.hc_api.package_name = "nodejs-imagestreams"
        self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "nodejs-application"
        assert self.hc_api.helm_package()
        pod_name = f"nodejs-ex-{version}".replace("-minimal", "")
        assert self.hc_api.helm_installation(
            values={
                "nodejs_version": version,
                "namespace": self.hc_api.namespace,
                "name": pod_name
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix=pod_name)
        assert self.hc_api.test_helm_curl_output(
            route_name=pod_name,
            expected_str="Node.js Crud Application"
        )

    @pytest.mark.parametrize(
        "version",
        [
            "20-ubi9",
            "20-ubi9-minimal"
            "20-ubi8",
            "20-ubi8-minimal",
            "18-ubi9",
            "18-ubi9-minimal",
            "18-ubi8",
            "18-ubi8-minimal",
        ],
    )
    def test_by_helm_test(self, version):
        self.hc_api.package_name = "nodejs-imagestreams"
        self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "nodejs-application"
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
