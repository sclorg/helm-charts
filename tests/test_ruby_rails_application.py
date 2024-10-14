import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmCakePHPTemplate:

    def setup_method(self):
        package_name = "ruby-rails-application"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,branch",
        [
            ("3.3-ubi9", "3.3"),
            ("3.3-ubi8", "3.3"),
            ("3.1-ubi9", "master"),
            ("3.1-ubi8", "master"),
            ("3.0-ubi9", "master"),
            ("2.5-ubi8", "master"),
        ],
    )
    def test_curl_connection(self, version, branch):
        if self.hc_api.oc_api.shared_cluster:
            pytest.skip("Do NOT test on shared cluster")
        self.hc_api.package_name = "ruby-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "ruby-rails-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "ruby_version": f"{version}",
                "source_repository_ref": f"{branch}",
                "namespace": self.hc_api.namespace
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="rails-example")
        assert self.hc_api.test_helm_curl_output(
            route_name="rails-example",
            expected_str="Welcome to your Rails application"
        )

    @pytest.mark.parametrize(
        "version,branch",
        [
            ("3.3-ubi9", "3.3"),
            ("3.3-ubi8", "3.3"),
            ("3.1-ubi9", "master"),
            ("3.1-ubi8", "master"),
            ("3.0-ubi9", "master"),
            ("2.5-ubi8", "master"),
        ],
    )
    def test_by_helm_test(self, version, branch):
        self.hc_api.package_name = "ruby-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "ruby-rails-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "ruby_version": f"{version}",
                "source_repository_ref": f"{branch}",
                "namespace": self.hc_api.namespace
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="rails-example")
        assert self.hc_api.test_helm_chart(expected_str=["Welcome to your Rails application"])
