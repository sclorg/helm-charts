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

    def test_curl_connection(self):
        self.hc_api.package_name = "nodejs-imagestreams"
        self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "nodejs-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "nodejs_version": "20-ubi8",
                "namespace": self.hc_api.namespace
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="nodejs-example")
        assert self.hc_api.test_helm_curl_output(
            route_name="nodejs-example",
            expected_str="Node.js Crud Application"
        )

    def test_by_helm_test(self):
        self.hc_api.package_name = "nodejs-imagestreams"
        self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "nodejs-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "nodejs": "20-ubi8",
                "namespace": self.hc_api.namespace
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="nodejs-example")
        assert self.hc_api.test_helm_chart(expected_str=["Node.js Crud Application"])
