import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmPythonDjangoAppTemplate:

    def setup_method(self):
        package_name = "python-django-application"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    def test_django_application_curl_output(self):
        if self.hc_api.oc_api.shared_cluster:
            pytest.skip("Do NOT test on shared cluster")
        self.hc_api.package_name = "python-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "python-django-application"
        self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "python_version": "3.11-ubi8",
                "namespace": self.hc_api.namespace
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="django-example")
        assert self.hc_api.test_helm_curl_output(
            route_name="django-example",
            expected_str="Welcome to your Django application"
        )

    def test_django_application_helm_test(self):
        self.hc_api.package_name = "python-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "python-django-application"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "python_version": "3.11-ubi8",
                "namespace": self.hc_api.namespace
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix="django-example")
        assert self.hc_api.test_helm_chart(expected_str=["Welcome to your Django application"])
