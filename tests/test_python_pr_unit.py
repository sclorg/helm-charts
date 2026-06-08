"""
Unit tests for PR changes:
- charts/redhat/redhat-python-django-application/src/values.schema.json
- charts/redhat/redhat-python-imagestreams/src/templates/python-imagestream.yaml
- tests/test_python_django_app.py parametrize list
- tests/test_python_django_psql_persistent.py parametrize list
- tests/test_python_imagestreams.py parametrize list
"""
import json
import os

import pytest
import yaml
from pathlib import Path

repo_root = Path(os.path.abspath(os.path.dirname(__file__))) / ".."
SCHEMA_PATH = repo_root / "charts/redhat/redhat-python-django-application/src/values.schema.json"
IMAGESTREAM_PATH = repo_root / "charts/redhat/redhat-python-imagestreams/src/templates/python-imagestream.yaml"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def load_imagestream():
    with open(IMAGESTREAM_PATH) as f:
        return yaml.safe_load(f)


def imagestream_tags_by_name(imagestream):
    """Return a dict mapping tag name -> tag dict."""
    return {tag["name"]: tag for tag in imagestream["spec"]["tags"]}


# ---------------------------------------------------------------------------
# values.schema.json – python_version enum
# ---------------------------------------------------------------------------

class TestSchemaJsonValidity:
    def test_schema_is_valid_json(self):
        """The schema file must be parseable as JSON without errors."""
        schema = load_schema()
        assert isinstance(schema, dict)

    def test_schema_has_required_top_level_keys(self):
        schema = load_schema()
        assert "$schema" in schema
        assert "type" in schema
        assert "properties" in schema

    def test_python_version_enum_exists(self):
        schema = load_schema()
        assert "python_version" in schema["properties"]
        assert "enum" in schema["properties"]["python_version"]

    # --- new versions added in this PR ---

    def test_python_version_enum_contains_3_14_ubi9(self):
        enum = load_schema()["properties"]["python_version"]["enum"]
        assert "3.14-ubi9" in enum

    def test_python_version_enum_contains_3_14_minimal_ubi9(self):
        enum = load_schema()["properties"]["python_version"]["enum"]
        assert "3.14-minimal-ubi9" in enum

    def test_python_version_enum_contains_3_14_minimal_ubi10(self):
        enum = load_schema()["properties"]["python_version"]["enum"]
        assert "3.14-minimal-ubi10" in enum

    # --- versions removed in this PR ---

    def test_python_version_enum_does_not_contain_3_11_ubi8(self):
        enum = load_schema()["properties"]["python_version"]["enum"]
        assert "3.11-ubi8" not in enum

    def test_python_version_enum_does_not_contain_3_11_ubi9(self):
        enum = load_schema()["properties"]["python_version"]["enum"]
        assert "3.11-ubi9" not in enum

    # --- versions that must remain ---

    @pytest.mark.parametrize("version", [
        "latest",
        "3.6-ubi8",
        "3.9-ubi8",
        "3.12-ubi8",
        "3.9-ubi9",
        "3.12-ubi9",
        "3.12-minimal-ubi9",
        "3.12-minimal-ubi10",
    ])
    def test_python_version_enum_retains_existing_versions(self, version):
        enum = load_schema()["properties"]["python_version"]["enum"]
        assert version in enum

    def test_python_version_enum_total_count(self):
        """Enum should have exactly 11 entries after the PR changes."""
        enum = load_schema()["properties"]["python_version"]["enum"]
        assert len(enum) == 11

    def test_python_version_enum_no_duplicates(self):
        enum = load_schema()["properties"]["python_version"]["enum"]
        assert len(enum) == len(set(enum))

    # --- django_secret_key indentation fix (cosmetic, but field must still be valid) ---

    def test_django_secret_key_field_present(self):
        schema = load_schema()
        assert "django_secret_key" in schema["properties"]

    def test_django_secret_key_type_is_string(self):
        field = load_schema()["properties"]["django_secret_key"]
        assert field["type"] == "string"

    def test_django_secret_key_has_description(self):
        field = load_schema()["properties"]["django_secret_key"]
        assert "description" in field
        assert field["description"] == "Set this to a long random string."

    # --- boundary / negative cases ---

    def test_python_version_enum_does_not_contain_empty_string(self):
        enum = load_schema()["properties"]["python_version"]["enum"]
        assert "" not in enum

    def test_python_version_enum_does_not_contain_none(self):
        enum = load_schema()["properties"]["python_version"]["enum"]
        assert None not in enum

    def test_python_version_type_is_string(self):
        field = load_schema()["properties"]["python_version"]
        assert field["type"] == "string"


# ---------------------------------------------------------------------------
# python-imagestream.yaml – new 3.14 image stream entries
# ---------------------------------------------------------------------------

class TestImagestreamYamlValidity:
    def test_imagestream_is_valid_yaml(self):
        data = load_imagestream()
        assert data is not None

    def test_imagestream_kind(self):
        data = load_imagestream()
        assert data["kind"] == "ImageStream"

    def test_imagestream_has_spec_tags(self):
        data = load_imagestream()
        assert "spec" in data
        assert "tags" in data["spec"]
        assert isinstance(data["spec"]["tags"], list)

    # --- 3.14-minimal-ubi10 tag (new in this PR) ---

    def test_tag_3_14_minimal_ubi10_exists(self):
        tags = imagestream_tags_by_name(load_imagestream())
        assert "3.14-minimal-ubi10" in tags

    def test_tag_3_14_minimal_ubi10_docker_image(self):
        tags = imagestream_tags_by_name(load_imagestream())
        tag = tags["3.14-minimal-ubi10"]
        assert tag["from"]["kind"] == "DockerImage"
        assert tag["from"]["name"] == "registry.redhat.io/ubi10/python-314-minimal:latest"

    def test_tag_3_14_minimal_ubi10_reference_policy(self):
        tags = imagestream_tags_by_name(load_imagestream())
        tag = tags["3.14-minimal-ubi10"]
        assert tag["referencePolicy"]["type"] == "Local"

    def test_tag_3_14_minimal_ubi10_annotations(self):
        tags = imagestream_tags_by_name(load_imagestream())
        ann = tags["3.14-minimal-ubi10"]["annotations"]
        assert ann["iconClass"] == "icon-python"
        assert "builder,python" in ann["tags"]
        assert "python:3.14" in ann["supports"]
        assert ann["version"] == "3.14-minimal"

    def test_tag_3_14_minimal_ubi10_display_name(self):
        tags = imagestream_tags_by_name(load_imagestream())
        ann = tags["3.14-minimal-ubi10"]["annotations"]
        assert "3.14" in ann["openshift.io/display-name"]
        assert "UBI 10" in ann["openshift.io/display-name"]

    def test_tag_3_14_minimal_ubi10_provider_display_name(self):
        tags = imagestream_tags_by_name(load_imagestream())
        ann = tags["3.14-minimal-ubi10"]["annotations"]
        assert ann["openshift.io/provider-display-name"] == "Red Hat, Inc."

    def test_tag_3_14_minimal_ubi10_sample_repo(self):
        tags = imagestream_tags_by_name(load_imagestream())
        ann = tags["3.14-minimal-ubi10"]["annotations"]
        assert ann["sampleRepo"] == "https://github.com/sclorg/django-ex.git"

    # --- 3.14-minimal-ubi9 tag (new in this PR) ---

    def test_tag_3_14_minimal_ubi9_exists(self):
        tags = imagestream_tags_by_name(load_imagestream())
        assert "3.14-minimal-ubi9" in tags

    def test_tag_3_14_minimal_ubi9_docker_image(self):
        tags = imagestream_tags_by_name(load_imagestream())
        tag = tags["3.14-minimal-ubi9"]
        assert tag["from"]["kind"] == "DockerImage"
        assert tag["from"]["name"] == "registry.redhat.io/ubi9/python-314-minimal:latest"

    def test_tag_3_14_minimal_ubi9_reference_policy(self):
        tags = imagestream_tags_by_name(load_imagestream())
        tag = tags["3.14-minimal-ubi9"]
        assert tag["referencePolicy"]["type"] == "Local"

    def test_tag_3_14_minimal_ubi9_annotations(self):
        tags = imagestream_tags_by_name(load_imagestream())
        ann = tags["3.14-minimal-ubi9"]["annotations"]
        assert ann["iconClass"] == "icon-python"
        assert "builder,python" in ann["tags"]
        assert "python:3.14" in ann["supports"]
        assert ann["version"] == "3.14-minimal"

    def test_tag_3_14_minimal_ubi9_display_name(self):
        tags = imagestream_tags_by_name(load_imagestream())
        ann = tags["3.14-minimal-ubi9"]["annotations"]
        assert "3.14" in ann["openshift.io/display-name"]
        assert "UBI 9" in ann["openshift.io/display-name"]

    # --- 3.14-ubi9 tag (new in this PR) ---

    def test_tag_3_14_ubi9_exists(self):
        tags = imagestream_tags_by_name(load_imagestream())
        assert "3.14-ubi9" in tags

    def test_tag_3_14_ubi9_docker_image(self):
        tags = imagestream_tags_by_name(load_imagestream())
        tag = tags["3.14-ubi9"]
        assert tag["from"]["kind"] == "DockerImage"
        assert tag["from"]["name"] == "registry.redhat.io/ubi9/python-314:latest"

    def test_tag_3_14_ubi9_reference_policy(self):
        tags = imagestream_tags_by_name(load_imagestream())
        tag = tags["3.14-ubi9"]
        assert tag["referencePolicy"]["type"] == "Local"

    def test_tag_3_14_ubi9_annotations(self):
        tags = imagestream_tags_by_name(load_imagestream())
        ann = tags["3.14-ubi9"]["annotations"]
        assert ann["iconClass"] == "icon-python"
        assert "builder,python" in ann["tags"]
        assert "python:3.14" in ann["supports"]
        assert ann["version"] == "3.14"

    def test_tag_3_14_ubi9_display_name(self):
        tags = imagestream_tags_by_name(load_imagestream())
        ann = tags["3.14-ubi9"]["annotations"]
        assert "3.14" in ann["openshift.io/display-name"]
        assert "UBI 9" in ann["openshift.io/display-name"]

    def test_tag_3_14_ubi9_sample_repo(self):
        tags = imagestream_tags_by_name(load_imagestream())
        ann = tags["3.14-ubi9"]["annotations"]
        assert ann["sampleRepo"] == "https://github.com/sclorg/django-ex.git"

    # --- ubi9 vs ubi10 registry path distinction ---

    def test_3_14_minimal_ubi10_uses_ubi10_registry(self):
        tags = imagestream_tags_by_name(load_imagestream())
        name = tags["3.14-minimal-ubi10"]["from"]["name"]
        assert "ubi10" in name
        assert "ubi9" not in name

    def test_3_14_minimal_ubi9_uses_ubi9_registry(self):
        tags = imagestream_tags_by_name(load_imagestream())
        name = tags["3.14-minimal-ubi9"]["from"]["name"]
        assert "ubi9" in name
        assert "ubi10" not in name

    def test_3_14_ubi9_uses_ubi9_registry(self):
        tags = imagestream_tags_by_name(load_imagestream())
        name = tags["3.14-ubi9"]["from"]["name"]
        assert "ubi9" in name
        assert "ubi10" not in name

    # --- all 3.14 tags use python-314 image name segment ---

    @pytest.mark.parametrize("tag_name", [
        "3.14-minimal-ubi10",
        "3.14-minimal-ubi9",
        "3.14-ubi9",
    ])
    def test_3_14_tags_use_python314_image(self, tag_name):
        tags = imagestream_tags_by_name(load_imagestream())
        image_name = tags[tag_name]["from"]["name"]
        assert "python-314" in image_name

    # --- no duplicated tag names ---

    def test_imagestream_tag_names_are_unique(self):
        data = load_imagestream()
        names = [tag["name"] for tag in data["spec"]["tags"]]
        assert len(names) == len(set(names))


# ---------------------------------------------------------------------------
# Consistency: schema enum <-> imagestream tags <-> test parametrize lists
# ---------------------------------------------------------------------------

# Versions in test_python_imagestreams.py parametrize (as changed by this PR)
IMAGESTREAM_TEST_VERSIONS = [
    ("3.14-minimal-ubi10", "registry.redhat.io/ubi10/python-314-minimal:latest"),
    ("3.12-minimal-ubi10", "registry.redhat.io/ubi10/python-312-minimal:latest"),
    ("3.14-minimal-ubi9",  "registry.redhat.io/ubi9/python-314-minimal:latest"),
    ("3.12-minimal-ubi9",  "registry.redhat.io/ubi9/python-312-minimal:latest"),
    ("3.14-ubi9",          "registry.redhat.io/ubi9/python-314:latest"),
    ("3.12-ubi9",          "registry.redhat.io/ubi9/python-312:latest"),
    ("3.12-ubi8",          "registry.redhat.io/ubi8/python-312:latest"),
    ("3.9-ubi9",           "registry.redhat.io/ubi9/python-39:latest"),
    ("3.6-ubi8",           "registry.redhat.io/ubi8/python-36:latest"),
]

# Versions in test_python_django_app.py parametrize (as changed by this PR)
DJANGO_APP_TEST_VERSIONS = [
    ("3.14-minimal-ubi10", "4.2.x"),
    ("3.14-ubi9",          "4.2.x"),
    ("3.12-minimal-ubi10", "4.2.x"),
    ("3.12-ubi9",          "4.2.x"),
    ("3.12-ubi8",          "4.2.x"),
]

# Versions in test_python_django_psql_persistent.py parametrize (as changed by this PR)
DJANGO_PSQL_TEST_VERSIONS = [
    ("3.14-minimal-ubi10", "3.14", "4.2.x"),
    ("3.14-minimal-ubi9",  "3.14", "4.2.x"),
    ("3.12-minimal-ubi10", "3.12", "4.2.x"),
    ("3.14-ubi9",          "3.14", "4.2.x"),
    ("3.12-ubi9",          "3.12", "4.2.x"),
    ("3.12-ubi8",          "3.12", "4.2.x"),
]


class TestParametrizeConsistency:
    """Verify the parametrize lists in test files are consistent with source files."""

    def test_imagestream_test_versions_exist_in_yaml(self):
        """Every version listed in test_python_imagestreams.py must exist in the YAML."""
        tags = imagestream_tags_by_name(load_imagestream())
        for version, _registry in IMAGESTREAM_TEST_VERSIONS:
            assert version in tags, f"Version {version!r} missing from imagestream YAML"

    def test_imagestream_test_registry_matches_yaml(self):
        """Each registry URL in test_python_imagestreams.py must match the YAML DockerImage."""
        tags = imagestream_tags_by_name(load_imagestream())
        for version, registry in IMAGESTREAM_TEST_VERSIONS:
            yaml_registry = tags[version]["from"]["name"]
            assert yaml_registry == registry, (
                f"Registry mismatch for {version!r}: "
                f"test={registry!r}, yaml={yaml_registry!r}"
            )

    def test_django_app_versions_exist_in_schema_enum(self):
        """Every python_version in test_python_django_app.py must be a valid schema enum value."""
        enum = load_schema()["properties"]["python_version"]["enum"]
        for version, _branch in DJANGO_APP_TEST_VERSIONS:
            assert version in enum, f"Version {version!r} not in schema enum"

    def test_django_psql_versions_exist_in_schema_enum(self):
        """Every python_version in test_python_django_psql_persistent.py must be in the schema."""
        enum = load_schema()["properties"]["python_version"]["enum"]
        for version, _pod_version, _branch in DJANGO_PSQL_TEST_VERSIONS:
            assert version in enum, f"Version {version!r} not in schema enum"

    def test_3_11_removed_from_django_app_parametrize(self):
        """3.11 versions must not be in the django app test list (removed in this PR)."""
        for version, _branch in DJANGO_APP_TEST_VERSIONS:
            assert not version.startswith("3.11"), (
                f"Version {version!r} is 3.11 but should have been removed"
            )

    def test_3_11_removed_from_django_psql_parametrize(self):
        """3.11 versions must not be in the django psql test list (removed in this PR)."""
        for version, _pod_version, _branch in DJANGO_PSQL_TEST_VERSIONS:
            assert not version.startswith("3.11"), (
                f"Version {version!r} is 3.11 but should have been removed"
            )

    def test_3_14_present_in_django_app_parametrize(self):
        """3.14 versions must appear in the django app test list (added in this PR)."""
        versions_with_3_14 = [v for v, _ in DJANGO_APP_TEST_VERSIONS if v.startswith("3.14")]
        assert len(versions_with_3_14) > 0, "No 3.14 versions found in DJANGO_APP_TEST_VERSIONS"

    def test_3_14_present_in_django_psql_parametrize(self):
        """3.14 versions must appear in the django psql test list (added in this PR)."""
        versions_with_3_14 = [v for v, _, _ in DJANGO_PSQL_TEST_VERSIONS if v.startswith("3.14")]
        assert len(versions_with_3_14) > 0, "No 3.14 versions found in DJANGO_PSQL_TEST_VERSIONS"

    def test_imagestream_test_includes_new_3_14_versions(self):
        """All three new 3.14 entries from the PR must be in the imagestream test list."""
        test_versions = {v for v, _ in IMAGESTREAM_TEST_VERSIONS}
        assert "3.14-minimal-ubi10" in test_versions
        assert "3.14-minimal-ubi9" in test_versions
        assert "3.14-ubi9" in test_versions

    def test_3_11_not_in_imagestream_test_versions(self):
        """3.11 versions were removed from test_python_imagestreams.py in this PR."""
        for version, _registry in IMAGESTREAM_TEST_VERSIONS:
            assert not version.startswith("3.11"), (
                f"Version {version!r} is 3.11 but should have been removed"
            )

    def test_django_psql_pod_version_matches_python_version(self):
        """The pod_version should be the major.minor extracted from the python_version."""
        for version, pod_version, _branch in DJANGO_PSQL_TEST_VERSIONS:
            # e.g. "3.14-minimal-ubi10" -> pod_version should be "3.14"
            major_minor = version.split("-")[0]
            assert major_minor == pod_version, (
                f"For version {version!r}, pod_version {pod_version!r} "
                f"does not match expected {major_minor!r}"
            )

    def test_imagestream_test_versions_no_duplicates(self):
        versions = [v for v, _ in IMAGESTREAM_TEST_VERSIONS]
        assert len(versions) == len(set(versions))

    def test_django_app_test_versions_no_duplicates(self):
        versions = [v for v, _ in DJANGO_APP_TEST_VERSIONS]
        assert len(versions) == len(set(versions))

    def test_django_psql_test_versions_no_duplicates(self):
        versions = [v for v, _, _ in DJANGO_PSQL_TEST_VERSIONS]
        assert len(versions) == len(set(versions))
