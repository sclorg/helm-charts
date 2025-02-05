import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmCakePHPTemplate:

    def setup_method(self):
        package_name = "redhat-php-cakephp-application"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version",
        [
            "8.0-ubi9",
            "8.2-ubi8",
            "8.2-ubi9",
        ]
    )
    def test_curl_connection(self, version):
        if self.hc_api.oc_api.shared_cluster:
            pytest.skip("Do NOT test on shared cluster")
        branch_to_test = "4.X"
        check_msg = "Welcome to CakePHP 4.5"
        if version.startswith("8.2") or version.startswith("8.3"):
            branch_to_test = "5.X"
            check_msg = "Welcome to CakePHP 4.5"
        self.hc_api.package_name = "redhat-php-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-php-cakephp-application"
        assert self.hc_api.helm_package()
        pod_name = f"cakephp-ex-{version}".replace(".", "-")
        assert self.hc_api.helm_installation(
            values={
                "php_version": version,
                "namespace": self.hc_api.namespace,
                "source_repository_ref": branch_to_test,
                "name": pod_name
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix=pod_name)
        assert self.hc_api.test_helm_curl_output(
            route_name=pod_name,
            expected_str=check_msg
        )

    @pytest.mark.parametrize(
        "version",
        [
            "8.0-ubi9",
            "8.1-ubi9",
            "8.2-ubi8",
            "8.2-ubi9",
        ]
    )
    def test_by_helm_test(self, version):
        branch_to_test = "4.X"
        check_msg = "Welcome to CakePHP 4.5"
        if version.startswith("8.2") or version.startswith("8.3"):
            branch_to_test = "5.X"
            check_msg = "Welcome to CakePHP"
        self.hc_api.package_name = "redhat-php-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-php-cakephp-application"
        assert self.hc_api.helm_package()
        pod_name = f"cakephp-ex-{version}".replace(".", "-")
        assert self.hc_api.helm_installation(
            values={
                "php_version": version,
                "namespace": self.hc_api.namespace,
                "source_repository_ref": branch_to_test,
                "name": pod_name
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix=pod_name)
        assert self.hc_api.test_helm_chart(expected_str=[check_msg])
