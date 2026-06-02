import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmPerlDancerMysqlAppTemplate:

    def setup_method(self):
        package_name = "redhat-perl-dancer-application"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, tarball_dir=test_dir, shared_cluster=True)

    def teardown_method(self):
        self.hc_api.delete_project()

    @pytest.mark.parametrize(
        "version",
        [
            "5.32-ubi9",
            "5.32-ubi8",
            "5.26-ubi8",
        ]
    )
    def test_dancer_application_helm_test(self, version):
        self.hc_api.package_name = "redhat-perl-imagestreams"
        assert self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.package_name = "redhat-perl-dancer-application"
        assert self.hc_api.helm_package()
        pod_name = f"dancer-ex-{version}".replace(".", "-")
        assert self.hc_api.helm_installation(
            values={
                "perl_version": version,
                "namespace": self.hc_api.namespace,
                "name": pod_name
            }
        )
        assert self.hc_api.is_s2i_pod_running(pod_name_prefix=pod_name, timeout=600)
        assert self.hc_api.test_helm_chart(expected_str=["Welcome to your Dancer application"])
