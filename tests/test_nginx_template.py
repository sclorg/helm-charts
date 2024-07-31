import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmNginxTemplate:

    def setup_method(self):
        package_name = "nginx-template"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    def test_curl_connection(self):
        self.hc_api.package_name = "nginx-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "nginx-template"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "nginx_version": "1.20-ubi8",
                "namespace": self.hc_api.namespace
            }
        )
        expected_str = "Welcome to your static nginx application on OpenShift"
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="nginx-example")
        assert self.hc_api.test_helm_curl_output(
            route_name="nginx-example",
            expected_str=expected_str
        )

    def test_helm_connection(self):
        self.hc_api.package_name = "nginx-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "nginx-template"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "nginx_version": "1.20-ubi8",
                "namespace": self.hc_api.namespace
            }
        )
        expected_str = "Welcome to your static nginx application on OpenShift"
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="nginx-example")
        assert self.hc_api.test_helm_chart(expected_str=[expected_str])
