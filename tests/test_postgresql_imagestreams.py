import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="module")
def helm_api(request):
    helm_api = HelmChartsAPI(path=test_dir / "../charts/redhat", package_name="redhat-postgresql-imagestreams", tarball_dir=test_dir)
    # app_name = os.path.basename(request.param)
    yield helm_api
    pass
    helm_api.delete_project()


class TestHelmRHELPostgresqlImageStreams:


    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("10-el8", "registry.redhat.io/rhel8/postgresql-10:latest", False),
            ("13-el8", "registry.redhat.io/rhel8/postgresql-13:latest", True),
            ("13-el9", "registry.redhat.io/rhel9/postgresql-13:latest", True),
            ("15-el8", "registry.redhat.io/rhel8/postgresql-15:latest", True),
            ("15-el9", "registry.redhat.io/rhel9/postgresql-15:latest", True),
            ("16-el8", "registry.redhat.io/rhel8/postgresql-16:latest", True),
            ("16-el9", "registry.redhat.io/rhel9/postgresql-16:latest", True),
        ],
    )
    def test_package_imagestream(self, helm_api, version, registry, expected):
        assert helm_api.helm_package()
        assert helm_api.helm_installation()
        assert helm_api.check_imagestreams(version=version, registry=registry) == expected
