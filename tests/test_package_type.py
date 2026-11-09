from ota_proto import update_metadata_pb2
from package_type import (
    FULL,
    INCREMENTAL,
    classify_metadata,
    classify_package,
    manifest_is_incremental,
)


def make_manifest(operation_types, with_src_extent=False):
    manifest = update_metadata_pb2.DeltaArchiveManifest()
    partition = manifest.partitions.add()
    partition.partition_name = "system"
    for operation_type in operation_types:
        operation = partition.operations.add()
        operation.type = operation_type
        if with_src_extent and operation_type == 0:
            operation.src_extents.add(start_block=0, num_blocks=1)
    return manifest


class TestClassifyMetadata:
    def test_pre_build_means_incremental(self):
        metadata = {"pre-build": "OnePlus/...:user/release-keys"}

        assert classify_metadata(metadata) == INCREMENTAL

    def test_pre_build_incremental_means_incremental(self):
        metadata = {"pre-build-incremental": "B.R4T3.123"}

        assert classify_metadata(metadata) == INCREMENTAL

    def test_full_metadata_is_unknown_without_payload(self):
        metadata = {"post-build": "OnePlus/...:user/release-keys"}

        assert classify_metadata(metadata) is None


class TestManifestIsIncremental:
    def test_source_copy_operation(self):
        assert manifest_is_incremental(make_manifest([4])) is True

    def test_bsdiff_operation(self):
        assert manifest_is_incremental(make_manifest([3])) is True

    def test_source_extents_on_replace_operation(self):
        assert manifest_is_incremental(
            make_manifest([0], with_src_extent=True)
        ) is True

    def test_full_payload_operations(self):
        assert manifest_is_incremental(make_manifest([0, 6, 8])) is False


class TestClassifyPackage:
    def test_metadata_wins(self):
        manifest = make_manifest([0])

        assert classify_package({"pre-build": "x"}, manifest) == INCREMENTAL

    def test_manifest_marks_incremental(self):
        assert classify_package({}, make_manifest([5])) == INCREMENTAL

    def test_manifest_marks_full(self):
        assert classify_package({}, make_manifest([0, 8])) == FULL

    def test_no_data_is_unknown(self):
        assert classify_package(None, None) is None
