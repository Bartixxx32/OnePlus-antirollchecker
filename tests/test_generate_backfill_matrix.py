from generate_backfill_matrix import split_into_shards


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
