import pytest

import ou_history
from generate_backfill_matrix import build_backfill_entries, select_versions


class FakeResponse:
    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self.data


class FakeSession:
    def __init__(self, responses):
        self.responses = dict(responses)
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append(url)
        seed = url.rsplit("/", 1)[-1]
        return FakeResponse(self.responses[seed])


class TestVersionSortKey:
    def test_orders_android_versions(self):
        versions = [
            "CPH2655_15.0.0.703(EX01)",
            "CPH2655_16.0.10.600(EX01)",
            "CPH2655_16.0.2.403(EX01)",
            "CPH2655_17.0.0.102(EX01)",
            "CPH2655_15.0.0.862(EX01)",
        ]

        assert sorted(versions, key=ou_history.version_sort_key, reverse=True) == [
            "CPH2655_17.0.0.102(EX01)",
            "CPH2655_16.0.10.600(EX01)",
            "CPH2655_16.0.2.403(EX01)",
            "CPH2655_15.0.0.862(EX01)",
            "CPH2655_15.0.0.703(EX01)",
        ]

    def test_unparseable_codename_sorts_last(self):
        versions = ["CPH2611_11_A.65", "CPH2611_16.0.5.1301(EX01)"]

        assert sorted(versions, key=ou_history.version_sort_key, reverse=True) == [
            "CPH2611_16.0.5.1301(EX01)",
            "CPH2611_11_A.65",
        ]


class TestWalkChain:
    def test_follows_ota_version_until_exhausted(self):
        session = FakeSession({
            "seed1": {
                "version_number": "CPH2583_15.0.0.503(EX01)",
                "ota_version_number": "seed2",
                "download_url": "https://example.test/503.zip",
            },
            "seed2": {
                "version_number": "CPH2583_15.0.0.510(EX01)",
                "ota_version_number": "seed3",
                "download_url": "https://example.test/510.zip",
            },
            "seed3": {
                "information": "unable to find a more recent build",
            },
        })

        packages = ou_history.walk_chain(130, "seed1", session=session)

        assert [p["version"] for p in packages] == [
            "CPH2583_15.0.0.503(EX01)",
            "CPH2583_15.0.0.510(EX01)",
        ]
        assert packages[0]["from_version"] == "seed1"
        assert packages[1]["from_version"] == "seed2"
        assert len(session.calls) == 3

    def test_stops_on_repeated_seed(self):
        session = FakeSession({
            "seed1": {
                "version_number": "V2",
                "ota_version_number": "seed1",
                "download_url": "https://example.test/v2.zip",
            },
        })

        packages = ou_history.walk_chain(130, "seed1", session=session)

        assert len(packages) == 1


class TestGetHistoryPackages:
    def test_merges_chain_archive_and_latest_without_duplicates(self, monkeypatch):
        monkeypatch.setattr(ou_history, "OU_NA_DEVICE_IDS", {"13": 154})
        monkeypatch.setattr(ou_history, "HISTORY_SEEDS", {"13": ["seed1"]})
        monkeypatch.setattr(
            ou_history,
            "ARCHIVE_PACKAGES",
            {
                "13": [
                    {
                        "version": "CPH2655_15.0.0.405(EX01)",
                        "url": "https://example.test/405.zip",
                    }
                ]
            },
        )
        monkeypatch.setattr(
            ou_history,
            "walk_chain",
            lambda *args, **kwargs: [
                {
                    "version": "CPH2655_15.0.0.703(EX01)",
                    "url": "https://example.test/703.zip",
                }
            ],
        )
        monkeypatch.setattr(
            ou_history,
            "get_latest_package",
            lambda *args, **kwargs: {
                "version": "CPH2655_16.0.10.600(EX01)",
                "url": "https://example.test/latest.zip",
            },
        )

        packages = ou_history.get_history_packages("13", session=object())

        assert {p["version"] for p in packages} == {
            "CPH2655_15.0.0.405(EX01)",
            "CPH2655_15.0.0.703(EX01)",
            "CPH2655_16.0.10.600(EX01)",
        }

    def test_unknown_device_returns_empty(self):
        assert ou_history.get_history_packages("15T") == []


class TestNaMatrixEntries:
    def test_builds_ou_entries_with_direct_urls(self):
        packages = [
            {
                "version": "CPH2655_16.0.10.600(EX01)",
                "url": "https://example.test/new.zip",
                "md5": "abc123",
            },
            {"version": "CPH2655_15.0.0.405(EX01)", "url": "https://example.test/old.zip"},
        ]

        entries = ou_history.build_ou_matrix_entries(
            "13", "OnePlus 13", "NA", packages, 1, select_versions
        )

        assert entries == [
            {
                "device": "13",
                "variant": "NA",
                "device_short": "13",
                "device_name": "OnePlus 13",
                "version": "CPH2655_16.0.10.600(EX01)",
                "source": "ou_url",
                "url": "https://example.test/new.zip",
                "md5": "abc123",
                "ou_device_id": 154,
                "ota_version": None,
            }
        ]

    def test_backfill_matrix_uses_ou_for_na_and_springer_for_rest(self, monkeypatch):
        monkeypatch.setattr(
            "generate_backfill_matrix.DEVICE_METADATA",
            {
                "13": {
                    "name": "OnePlus 13",
                    "models": {"NA": "CPH2655", "GLO": "CPH2653"},
                }
            },
        )
        monkeypatch.setattr(
            "generate_backfill_matrix.get_na_packages",
            lambda *args, **kwargs: [
                {"version": "CPH2655_16.0.10.600(EX01)", "url": "https://example.test/na.zip"}
            ],
        )
        monkeypatch.setattr(
            "generate_backfill_matrix.get_springer_versions",
            lambda *args, **kwargs: (
                ["CPH2653_16.0.10.601(EX01)"],
                "OP 13",
            ),
        )
        monkeypatch.setattr(
            "generate_backfill_matrix.OU_NA_DEVICE_IDS",
            {"13": 154},
        )

        entries = build_backfill_entries(
            target_device="13", target_variant="", max_versions=10, session=object()
        )

        assert [entry["source"] for entry in entries] == ["ou_url", "springer"]
        assert entries[0]["variant"] == "NA"
        assert entries[1]["variant"] == "GLO"

    def test_target_variant_filters_regions(self, monkeypatch):
        monkeypatch.setattr(
            "generate_backfill_matrix.DEVICE_METADATA",
            {
                "13": {
                    "name": "OnePlus 13",
                    "models": {"NA": "CPH2655", "GLO": "CPH2653"},
                }
            },
        )
        monkeypatch.setattr(
            "generate_backfill_matrix.get_na_packages",
            lambda *args, **kwargs: [],
        )
        monkeypatch.setattr(
            "generate_backfill_matrix.OU_NA_DEVICE_IDS",
            {"13": 154},
        )

        entries = build_backfill_entries(
            target_device="13", target_variant="na", max_versions=10, session=object()
        )

        assert entries == []
