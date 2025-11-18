import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmPythonDjangoPsqlTemplate:
    def setup_method(self):
        package_name = "redhat-django-psql-persistent"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(
            path=path,
            package_name=package_name,
            tarball_dir=test_dir,
            shared_cluster=False,
        )

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version,pod_version,branch",
        [
            ("3.12-minimal-ubi10", "3.12", "4.2.x"),
            ("3.12-ubi9", "3.12", "4.2.x"),
            ("3.12-ubi8", "3.12", "4.2.x"),
            ("3.11-ubi9", "3.11", "4.2.x"),
            ("3.11-ubi8", "3.11", "4.2.x"),
        ],
    )
    def test_django_psql_helm_test(self, version, pod_version, branch):
        self.hc_api.package_name = "redhat-postgresql-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-python-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-django-psql-persistent"
        assert self.hc_api.helm_package()
        pod_name = f"django-{pod_version}".replace(".", "-")
        assert self.hc_api.helm_installation(
            values={
                "python_version": version,
                "namespace": self.hc_api.namespace,
                "source_repository_ref": branch,
                "postgresql_version": "15-el9",
                "name": pod_name,
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix=pod_name, timeout=600)
        assert self.hc_api.test_helm_chart(
            expected_str=["Welcome to your Django application"]
        )
