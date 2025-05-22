import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmPostgresqlPersistent:

    def setup_method(self):
        package_name = "redhat-postgresql-persistent"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version",
        [
            "13-el8",
            "13-el9",
            "15-el8",
            "15-el9",
            "16-el8",
            "16-el9",
            "16-el10",
        ],
    )
    def test_package_persistent(self, version):
        self.hc_api.package_name = "redhat-postgresql-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-postgresql-persistent"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation(values={"image.tag": version, "namespace": self.hc_api.namespace})
        assert self.hc_api.is_pod_running(pod_name_prefix="redhat-postgresql-persistent")
        assert self.hc_api.test_helm_chart(expected_str=["accepting connection"])
