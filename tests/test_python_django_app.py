import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmPythonDjangoAppTemplate:

    def setup_method(self):
        package_name = "redhat-python-django-application"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir, shared_cluster=False)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,branch",
        [
            ("3.12-minimal-ubi10", "4.2.x"),
            ("3.12-ubi9", "4.2.x"),
            ("3.12-ubi8", "4.2.x"),
            ("3.11-ubi9", "4.2.x"),
            ("3.11-ubi8", "4.2.x"),
            ("3.9-ubi9", "master"),
            ("3.9-ubi8", "master"),
            ("3.6-ubi8", "master"),
        ],
    )
    def test_django_application_helm_test(self, version, branch):
        self.hc_api.package_name = "redhat-python-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-python-django-application"
        assert self.hc_api.helm_package()
        pod_name = f"django-{version}".replace(".", "-").replace("-minimal", "")
        assert self.hc_api.helm_installation(
            values={
                "python_version": version,
                "namespace": self.hc_api.namespace,
                "source_repository_ref": branch,
                "name": pod_name
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix=pod_name, timeout=600)
        assert self.hc_api.test_helm_chart(expected_str=["Welcome to your Django application"])
