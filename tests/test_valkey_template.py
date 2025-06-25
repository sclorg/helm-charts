import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmValkeyPersistent:

    def setup_method(self):
        package_name = "redhat-valkey-persistent"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir, shared_cluster=True)
        self.hc_api.package_name = "redhat-valkey-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version",
        [
            "8-el10",
        ],
    )
    def test_package_persistent(self, version):

        self.hc_api.package_name = "redhat-valkey-persistent"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(
            values={
                "valkey_version": version,
                "namespace": self.hc_api.namespace
            }
        )
        assert self.hc_api.is_pod_running(pod_name_prefix="valkey")
        assert self.hc_api.test_helm_chart(expected_str=["PONG"])
