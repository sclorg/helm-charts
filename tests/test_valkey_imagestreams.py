import pytest

from container_ci_suite.helm import HelmChartsAPI

from conftests import VARS


class TestHelmRHELOSValkeyImageStreams:
    def setup_method(self):
        package_name = "redhat-valkey-imagestreams"
        self.helm_api = HelmChartsAPI(
            path=VARS.TEST_DIR / "../charts/redhat",
            package_name=package_name,
            tarball_dir=VARS.TEST_DIR,
            shared_cluster=True,
        )

    def teardown_method(self):
        self.helm_api.delete_project()

    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("8-el10", "registry.redhat.io/rhel10/valkey-8:latest", True),
            ("8-el9", "registry.redhat.io/rhel9/valkey-8:latest", True),
        ],
    )
    def test_package_imagestream(self, version, registry, expected):
        assert self.helm_api.helm_package()
        assert self.helm_api.helm_installation()
        assert (
            self.helm_api.check_imagestreams(version=version, registry=registry) == expected
        )
