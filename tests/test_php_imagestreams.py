import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="module")
def helm_api(request):
    helm_api = HelmChartsAPI(path=test_dir / "../charts/redhat", package_name="redhat-php-imagestreams", tarball_dir=test_dir)
    # app_name = os.path.basename(request.param)
    yield helm_api
    pass
    helm_api.delete_project()


class TestHelmRHELPHPImageStreams:


    @pytest.mark.parametrize(
        "version,registry",
        [
            ("8.4-ubi10", "registry.redhat.io/ubi10/php-84:latest"),
            ("8.3-ubi10", "registry.redhat.io/ubi10/php-83:latest"),
            ("8.3-ubi9", "registry.redhat.io/ubi9/php-83:latest"),
            ("8.2-ubi9", "registry.redhat.io/ubi9/php-82:latest"),
            ("8.2-ubi8", "registry.redhat.io/ubi8/php-82:latest"),
            ("8.0-ubi9", "registry.redhat.io/ubi9/php-80:latest"),
            ("7.4-ubi8", "registry.redhat.io/ubi8/php-74:latest"),
        ],
    )
    def test_package_imagestream(self, helm_api,  version, registry):
        assert helm_api.helm_package()
        assert helm_api.helm_installation()
        assert helm_api.check_imagestreams(version=version, registry=registry) == True
