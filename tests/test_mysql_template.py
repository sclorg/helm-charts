import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmMySQLDBPersistent:

    def setup_method(self):
        package_name = "mysql-persistent"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version",
        [
            "8.0-el9",
            "8.0-el8",
        ],
    )
    def test_package_persistent(self, version):
        self.hc_api.package_name = "mysql-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "mysql-persistent"
        assert self.hc_api.helm_package()
        pod_name = f"mysql-{version}".replace(".", "")
        assert self.hc_api.helm_installation(
            values={
                "mysql_version": version,
                "namespace": self.hc_api.namespace,
                "name": pod_name
            }
        )
        assert self.hc_api.is_pod_running(pod_name_prefix=pod_name)
        assert self.hc_api.test_helm_chart(expected_str=["42", "testval"])
