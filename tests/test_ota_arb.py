import lzma

from ota_arb import _decompress


class TestDecompress:
    def test_replace_is_passthrough(self):
        assert _decompress(b"raw-bytes", 0) == b"raw-bytes"

    def test_replace_xz(self):
        payload = b"xbl-config-image" * 32

        assert _decompress(lzma.compress(payload), 8) == payload

    def test_replace_bz(self):
        import bz2

        payload = b"xbl-config-image" * 32

        assert _decompress(bz2.compress(payload), 1) == payload

    def test_unknown_operation_returns_none(self):
        assert _decompress(b"data", 99) is None
