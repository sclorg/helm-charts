import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="module")
def helm_api(request):
    helm_api = HelmChartsAPI(path=test_dir / "../charts/redhat", package_name="php-imagestreams", tarball_dir=test_dir)
    print(request)
    # app_name = os.path.basename(request.param)
    yield helm_api
    pass
    helm_api.delete_project()


class TestHelmRHELPHPImageStreams:


    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("8.2-ubi9", "registry.redhat.io/ubi9/php-82:latest", True),
            ("8.2-ubi8", "registry.redhat.io/ubi8/php-82:latest", True),
            ("8.1-ubi9", "registry.redhat.io/ubi9/php-81:latest", True),
            ("8.0-ubi9", "registry.redhat.io/ubi9/php-80:latest", True),
            ("8.0-ubi8", "registry.redhat.io/ubi8/php-80:latest", True),
            ("7.4-ubi8", "registry.redhat.io/ubi8/php-74:latest", True),
        ],
    )
    def test_package_imagestream(self, helm_api,  version, registry, expected):
        assert helm_api.helm_package()
        assert helm_api.helm_installation()
        assert helm_api.check_imagestreams(version=version, registry=registry) == expected
