from generate_backfill_matrix import (
    parse_max_versions,
    select_versions,
    split_into_shards,
)


class TestParseMaxVersions:
    def test_numeric_value(self):
        assert parse_max_versions("10") == 10

    def test_zero_means_all(self):
        assert parse_max_versions("0") is None

    def test_all_keywords_mean_all(self):
        assert parse_max_versions("all") is None
        assert parse_max_versions("wszystko") is None
        assert parse_max_versions("") is None

    def test_invalid_value_uses_default(self):
        assert parse_max_versions("abc") == 10

    def test_negative_means_all(self):
        assert parse_max_versions("-3") is None


class TestSelectVersions:
    def test_takes_newest_n(self):
        versions = ["v5", "v4", "v3", "v2", "v1"]

        assert select_versions(versions, 2) == ["v5", "v4"]

    def test_none_returns_all(self):
        versions = ["v5", "v4", "v3"]

        assert select_versions(versions, None) == versions

    def test_zero_returns_all(self):
        versions = ["v5", "v4", "v3"]

        assert select_versions(versions, 0) == versions

    def test_more_than_available_returns_all(self):
        versions = ["v2", "v1"]

        assert select_versions(versions, 10) == versions


class TestSplitIntoShards:
    def test_splits_all_items_without_loss_or_duplication(self):
        items = list(range(10))

        shards = split_into_shards(items, 4)

        assert [len(shard) for shard in shards] == [3, 3, 2, 2]
        assert sorted(item for shard in shards for item in shard) == items

    def test_empty_input_produces_empty_shards(self):
        assert split_into_shards([], 4) == [[], [], [], []]

    def test_single_shard_keeps_everything_together(self):
        items = ["a", "b", "c"]

        assert split_into_shards(items, 1) == [items]
