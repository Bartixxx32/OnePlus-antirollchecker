"""Tests for the local xbl_config ARB parser.

The fixtures are minimal synthetic ELF64 images that mimic the hash
segment layout of Qualcomm xbl_config images:

* legacy (hash-table v7): OEM metadata record at segment offset 0x40
* v8 (e.g. OnePlus 16):    an extra 16-byte record at 0x40 shifts the
                           OEM metadata record to 0x50
"""

import struct

import pytest

from arb_parser import parse_elf64_arb, parse_xbl_config_file

SEG_OFF = 0x200
SEG_SIZE = 0x200
HASH_HDR_OFF = 0x4  # parser locates the header by scanning, not hardcoded


def build_xbl_image(version, oem_record, extra_record=None):
    """Build a minimal ELF64 xbl_config image with a hash segment.

    ``oem_record`` is ``(major, minor, arb, reserved)``.  When
    ``extra_record`` is given it is placed at 0x40 and the OEM record is
    shifted to 0x50, reproducing the v8 layout.
    """
    common_size = 0x18
    oem_size = 0xE0

    seg = bytearray(SEG_SIZE)
    struct.pack_into(
        "<IIIII", seg, HASH_HDR_OFF,
        version, common_size, 0, oem_size, 0x120,
    )

    if extra_record is not None:
        struct.pack_into("<IIII", seg, 0x40, *extra_record)
        record_off = 0x50
    else:
        record_off = 0x40

    struct.pack_into("<IIII", seg, record_off, *oem_record)
    struct.pack_into("<I", seg, record_off + 0x10, 0xA023)

    elf = bytearray(SEG_OFF + SEG_SIZE)
    elf[0:4] = b"\x7fELF"
    elf[4] = 2  # ELFCLASS64
    struct.pack_into("<Q", elf, 0x20, 64)   # e_phoff
    struct.pack_into("<H", elf, 0x36, 56)   # e_phentsize
    struct.pack_into("<H", elf, 0x38, 1)    # e_phnum

    # Single PT_NULL program header pointing at the hash segment.
    struct.pack_into("<I", elf, 64, 0)          # p_type
    struct.pack_into("<Q", elf, 64 + 8, SEG_OFF)  # p_offset
    struct.pack_into("<Q", elf, 64 + 32, SEG_SIZE)  # p_filesz
    struct.pack_into("<Q", elf, 64 + 40, SEG_SIZE)  # p_memsz

    elf[SEG_OFF:SEG_OFF + SEG_SIZE] = seg
    return bytes(elf)


class TestParseElf64Arb:
    def test_legacy_v7_layout(self):
        image = build_xbl_image(7, (3, 0, 1, 0))
        assert parse_elf64_arb(image) == {"arb": 1, "major": 3, "minor": 0}

    def test_v8_layout_reads_shifted_record(self):
        # The extra record at 0x40 is the constant 0x25/0/3/0 block that
        # arbextract 1.0 misreads as major=37, arb=3.
        image = build_xbl_image(
            8,
            (4, 0, 0, 0),
            extra_record=(0x25, 0, 3, 0),
        )
        assert parse_elf64_arb(image) == {"arb": 0, "major": 4, "minor": 0}

    def test_v8_layout_does_not_return_misaligned_record(self):
        # A 4-byte-step scan would land on offset 0x48 and read
        # (major=3, minor=0, arb=4, reserved=0), which looks plausible.
        image = build_xbl_image(
            8,
            (4, 0, 0, 0),
            extra_record=(0x25, 0, 3, 0),
        )
        result = parse_elf64_arb(image)
        assert result["major"] == 4
        assert result["arb"] == 0

    def test_legacy_layout_allows_zero_major(self):
        image = build_xbl_image(6, (0, 0, 0, 0))
        assert parse_elf64_arb(image) == {"arb": 0, "major": 0, "minor": 0}

    def test_non_elf_returns_none(self):
        assert parse_elf64_arb(b"not an elf image" * 100) is None

    def test_truncated_image_returns_none(self):
        image = build_xbl_image(8, (4, 0, 0, 0), extra_record=(0x25, 0, 3, 0))
        assert parse_elf64_arb(image[:100]) is None


class TestParseXblConfigFile:
    def test_reads_file(self, tmp_path):
        path = tmp_path / "xbl_config.img"
        path.write_bytes(build_xbl_image(8, (4, 0, 0, 0), extra_record=(0x25, 0, 3, 0)))
        assert parse_xbl_config_file(str(path)) == {
            "arb": 0, "major": 4, "minor": 0,
        }

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(OSError):
            parse_xbl_config_file(str(tmp_path / "missing.img"))
