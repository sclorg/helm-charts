import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmHTTPDTemplate:

    def setup_method(self):
        package_name = "redhat-httpd-template"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir, shared_cluster=True)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version",
        [
            "2.4-el8",
            "2.4-el9",
        ],
    )
    def test_package_persistent_by_helm_chart_test(self, version):
        self.hc_api.package_name = "redhat-httpd-imagestreams"
        self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-httpd-template"
        self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "httpd_version": version,
                "namespace": self.hc_api.namespace,
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="httpd-example")
        assert self.hc_api.test_helm_chart(expected_str=["Welcome to your static httpd application on OpenShift"])
