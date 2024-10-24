import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmMariaDBPersistent:

    def setup_method(self):
        package_name = "mariadb-persistent"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)
        self.hc_api.package_name = "mariadb-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version",
        [
            "10.3-el8",
            "10.5-el8",
            "10.5-el9",
            "10.11-el8",
            "10.11-el9",
        ],
    )
    def test_package_persistent(self, version):
        self.hc_api.package_name = "mariadb-persistent"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "mariadb_version": version,
                "namespace": self.hc_api.namespace,
            }
        )
        assert self.hc_api.is_pod_running(pod_name_prefix="mariadb")
        assert self.hc_api.test_helm_chart(expected_str=["42", "testval"])
