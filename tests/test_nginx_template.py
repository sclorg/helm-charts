import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmNginxTemplate:

    def setup_method(self):
        package_name = "redhat-nginx-template"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version",
        [
            "1.24-ubi9",
            "1.24-ubi8",
            "1.22-ubi9",
            "1.22-ubi8",
            "1.20-ubi9",
        ]
    )
    def test_curl_connection(self, version):
        if self.hc_api.oc_api.shared_cluster:
            pytest.skip("Do NOT test on shared cluster")
        self.hc_api.package_name = "redhat-nginx-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-nginx-template"
        assert self.hc_api.helm_package()
        pod_name = f"nginx-ex-{version}".replace(".", "-")
        assert self.hc_api.helm_installation(
            values={
                "nginx_version": version,
                "namespace": self.hc_api.namespace,
                "name": pod_name
            }
        )
        expected_str = "Welcome to your static nginx application on OpenShift"
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix=pod_name)
        assert self.hc_api.test_helm_curl_output(
            route_name=pod_name,
            expected_str=expected_str
        )

    @pytest.mark.parametrize(
        "version",
        [
            "1.24-ubi9",
            "1.24-ubi8",
            "1.22-ubi9",
            "1.22-ubi8",
            "1.20-ubi9",
        ]
    )
    def test_helm_connection(self, version):
        self.hc_api.package_name = "redhat-nginx-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-nginx-template"
        assert self.hc_api.helm_package()
        pod_name = f"nginx-ex-{version}".replace(".", "-")
        assert self.hc_api.helm_installation(
            values={
                "nginx_version": version,
                "namespace": self.hc_api.namespace,
                "name": pod_name
            }
        )
        expected_str = "Welcome to your static nginx application on OpenShift"
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix=pod_name)
        assert self.hc_api.test_helm_chart(expected_str=[expected_str])
