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

    def test_curl_connection(self):
        self.hc_api.package_name = "ruby-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "ruby-rails-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "ruby_version": "3.1-ubi9",
                "namespace": self.hc_api.namespace
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="rails-example")
        assert self.hc_api.test_helm_curl_output(
            route_name="rails-example",
            expected_str="Welcome to your Rails application"
        )

    def test_by_helm_test(self):
        self.hc_api.package_name = "ruby-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "ruby-rails-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "ruby_version": "3.1-ubi9",
                "namespace": self.hc_api.namespace
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="rails-example")
        assert self.hc_api.test_helm_chart(expected_str=["Welcome to your Rails application"])
