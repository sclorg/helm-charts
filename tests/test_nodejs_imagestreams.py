import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="module")
def helm_api(request):
    helm_api = HelmChartsAPI(path=test_dir / "../charts/redhat", package_name="redhat-nodejs-imagestreams", tarball_dir=test_dir)
    print(request)
    # app_name = os.path.basename(request.param)
    yield helm_api
    pass
    helm_api.delete_project()

class TestHelmRHELNodeJSImageStreams:


    @pytest.mark.parametrize(
        "version,registry",
        [
            ("22-ubi9", "registry.redhat.io/ubi9/nodejs-22:latest"),
            ("22-ubi9-minimal", "registry.redhat.io/ubi9/nodejs-22-minimal:latest"),
            ("20-ubi9", "registry.redhat.io/ubi9/nodejs-20:latest"),
            ("20-ubi9-minimal", "registry.redhat.io/ubi9/nodejs-20-minimal:latest"),
            ("20-ubi8", "registry.redhat.io/ubi8/nodejs-20:latest"),
            ("20-ubi8-minimal", "registry.redhat.io/ubi8/nodejs-20-minimal:latest"),
            ("18-ubi9", "registry.redhat.io/ubi9/nodejs-18:latest"),
            ("18-ubi9-minimal", "registry.redhat.io/ubi9/nodejs-18-minimal:latest"),
            ("18-ubi8", "registry.redhat.io/ubi8/nodejs-18:latest"),
            ("18-ubi8-minimal", "registry.redhat.io/ubi8/nodejs-18-minimal:latest"),
        ],
    )
    def test_package_imagestream(self, helm_api, version, registry):
        assert helm_api.helm_package()
        assert helm_api.helm_installation()
        assert helm_api.check_imagestreams(version=version, registry=registry)
