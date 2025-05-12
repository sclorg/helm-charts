import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="module")
def helm_api(request):
    helm_api = HelmChartsAPI(path=test_dir / "../charts/redhat", package_name="redhat-httpd-imagestreams", tarball_dir=test_dir)
    # app_name = os.path.basename(request.param)
    yield helm_api
    pass
    helm_api.delete_project()

class TestHelmRHELHttpdImageStreams:

    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("2.4-ubi10", "registry.redhat.io/ubi10/httpd-24:latest", True),
            ("2.4-ubi9", "registry.redhat.io/ubi9/httpd-24:latest", True),
            ("2.4-ubi8", "registry.redhat.io/ubi8/httpd-24:latest", True),
            ("2.4-el8", "registry.redhat.io/rhel8/httpd-24", True),
            ("2.4-el9", "registry.redhat.io/rhel9/httpd-24", True),
            ("2.4-el10", "registry.redhat.io/rhel10/httpd-24", True),
        ],
    )
    def test_httpd_imagestream(self, helm_api, version, registry, expected):
        assert helm_api.helm_package()
        assert helm_api.helm_installation()
        assert helm_api.check_imagestreams(version=version, registry=registry) == expected
