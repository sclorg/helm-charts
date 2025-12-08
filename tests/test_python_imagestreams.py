import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="module")
def helm_api(request):
    helm_api = HelmChartsAPI(path=test_dir / "../charts/redhat", package_name="redhat-python-imagestreams", tarball_dir=test_dir)
    # app_name = os.path.basename(request.param)
    yield helm_api
    pass
    helm_api.delete_project()


class TestHelmRHELPythonImageStreams:


    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("3.12-minimal-ubi10", "registry.redhat.io/ubi10/python-312-minimal:latest", True),
            ("3.12-minimal-ubi9", "registry.redhat.io/ubi9/python-312-minimal:latest", True),
            ("3.12-ubi9", "registry.redhat.io/ubi9/python-312:latest", True),
            ("3.12-ubi8", "registry.redhat.io/ubi8/python-312:latest", True),
            ("3.11-ubi9", "registry.redhat.io/ubi9/python-311:latest", True),
            ("3.11-ubi8", "registry.redhat.io/ubi8/python-311:latest", True),
            ("3.9-ubi9", "registry.redhat.io/ubi9/python-39:latest", False),
            ("3.9-ubi8", "registry.redhat.io/ubi8/python-39:latest", True),
            ("3.6-ubi8", "registry.redhat.io/ubi8/python-36:latest", True),
        ],
    )
    def test_package_imagestream(self, helm_api, version, registry, expected):
        assert helm_api.helm_package()
        assert helm_api.helm_installation()
        assert helm_api.check_imagestreams(version=version, registry=registry) == expected
