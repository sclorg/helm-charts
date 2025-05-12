import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="module")
def helm_api(request):
    helm_api = HelmChartsAPI(path=test_dir / "../charts/redhat", package_name="redhat-nginx-imagestreams", tarball_dir=test_dir)
    # app_name = os.path.basename(request.param)
    yield helm_api
    pass
    helm_api.delete_project()

class TestHelmRHELNginxImageStreams:

    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("1.26-ubi10", "registry.redhat.io/ubi10/nginx-126:latest", True),
            ("1.26-ubi9", "registry.redhat.io/ubi9/nginx-126:latest", True),
            ("1.24-ubi9", "registry.redhat.io/ubi9/nginx-124:latest", True),
            ("1.24-ubi8", "registry.redhat.io/ubi8/nginx-124:latest", True),
            ("1.22-ubi9", "registry.redhat.io/ubi9/nginx-122:latest", True),
            ("1.22-ubi8", "registry.redhat.io/ubi8/nginx-122:latest", True),
            ("1.20-ubi9", "registry.redhat.io/ubi9/nginx-120:latest", True),
            ("1.20-ubi8", "registry.redhat.io/ubi8/nginx-120:latest", False),
        ],
    )
    def test_package_imagestream(self, helm_api, version, registry, expected):
        assert helm_api.helm_package()
        assert helm_api.helm_installation()
        assert helm_api.check_imagestreams(version=version, registry=registry) == expected
