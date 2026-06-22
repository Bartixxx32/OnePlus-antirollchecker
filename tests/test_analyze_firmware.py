import hashlib
import os
import pytest
import struct
import tempfile
import zipfile
import shutil
from pathlib import Path

from analyze_firmware import detect_file_type, calculate_md5, extract_ota_metadata


# ─── detect_file_type ─────────────────────────────────────────────────

class TestDetectFileType:
    def test_zip_magic(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'PK\x03\x04some zip content')
            path = f.name
        try:
            assert detect_file_type(Path(path)) == '.zip'
        finally:
            os.unlink(path)

    def test_zip_magic_empty_after_header(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'PK\x05\x06')  # EOCD marker also works
            path = f.name
        try:
            assert detect_file_type(Path(path)) == '.zip'
        finally:
            os.unlink(path)

    def test_7z_magic(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'\x37\x7a\xbc\xaf\x27\x1c\x00\x04')
            path = f.name
        try:
            assert detect_file_type(Path(path)) == '.7z'
        finally:
            os.unlink(path)

    def test_elf_magic(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'\x7f\x45\x4c\x46\x02\x01\x01\x00')
            path = f.name
        try:
            assert detect_file_type(Path(path)) == '.img'
        finally:
            os.unlink(path)

    def test_android_boot_magic(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'ANDROID! boot image data')
            path = f.name
        try:
            assert detect_file_type(Path(path)) == '.img'
        finally:
            os.unlink(path)

    def test_unknown_magic(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'\x00\x01\x02\x03\x04\x05\x06\x07')
            path = f.name
        try:
            assert detect_file_type(Path(path)) == ''
        finally:
            os.unlink(path)

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            path = f.name
        try:
            assert detect_file_type(Path(path)) == ''
        finally:
            os.unlink(path)

    def test_non_existent_file(self):
        assert detect_file_type(Path('/nonexistent/file.bin')) == ''

    def test_elf_shorter_header(self):
        """Only first 2 bytes match ELF but file is shorter."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'\x7f\x45')
            path = f.name
        try:
            assert detect_file_type(Path(path)) == '.img'
        finally:
            os.unlink(path)

    def test_url_encoded_filename(self):
        """Extension should not matter, magic bytes rule."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as f:
            f.write(b'\x37\x7a\xbc\xaf\x27\x1c\x00\x04')  # 7z magic with .zip extension
            path = f.name
        try:
            assert detect_file_type(Path(path)) == '.7z'
        finally:
            os.unlink(path)


# ─── calculate_md5 ────────────────────────────────────────────────────

class TestCalculateMd5:
    def test_empty_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            path = f.name
        try:
            expected = hashlib.md5(b'').hexdigest()
            assert calculate_md5(path) == expected
        finally:
            os.unlink(path)

    def test_simple_content(self):
        content = b'hello world'
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(content)
            path = f.name
        try:
            expected = hashlib.md5(content).hexdigest()
            assert calculate_md5(path) == expected
        finally:
            os.unlink(path)

    def test_large_content(self):
        content = b'x' * 100000  # 100KB
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(content)
            path = f.name
        try:
            expected = hashlib.md5(content).hexdigest()
            assert calculate_md5(path) == expected
        finally:
            os.unlink(path)

    def test_known_md5(self):
        content = b'The quick brown fox jumps over the lazy dog'
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(content)
            path = f.name
        try:
            # Known MD5 for this string
            expected = hashlib.md5(content).hexdigest()
            assert calculate_md5(path) == expected
        finally:
            os.unlink(path)


# ─── extract_ota_metadata ─────────────────────────────────────────────

class TestExtractOtaMetadata:
    def test_extract_metadata(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as f:
            path = f.name
        try:
            with zipfile.ZipFile(path, 'w') as z:
                z.writestr('META-INF/com/android/metadata', 
                           'pre-device=CPH2581\nproduct_name=OnePlus 12\npost-build=build123\n')
                z.writestr('payload_properties.txt', 'FILE_HASH=abc123\n')
            
            meta = extract_ota_metadata(path)
            assert meta['pre-device'] == 'CPH2581'
            assert meta['product_name'] == 'OnePlus 12'
            assert meta['post-build'] == 'build123'
            # payload_properties should not overwrite metadata fields
            assert 'FILE_HASH' in meta
        finally:
            os.unlink(path)

    def test_payload_properties_fallback(self):
        """When metadata is missing, fallback to payload_properties.txt."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as f:
            path = f.name
        try:
            with zipfile.ZipFile(path, 'w') as z:
                z.writestr('payload_properties.txt', 'FILE_HASH=abc123\nVERSION=14.0.0')
            
            meta = extract_ota_metadata(path)
            assert meta['FILE_HASH'] == 'abc123'
            assert meta['VERSION'] == '14.0.0'
        finally:
            os.unlink(path)

    def test_colon_delimiter_in_payload_properties(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as f:
            path = f.name
        try:
            with zipfile.ZipFile(path, 'w') as z:
                z.writestr('payload_properties.txt', 'FILE_HASH:abc123\nVERSION:14.0.0')
            
            meta = extract_ota_metadata(path)
            assert meta['FILE_HASH'] == 'abc123'
        finally:
            os.unlink(path)

    def test_empty_zip(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as f:
            path = f.name
        try:
            with zipfile.ZipFile(path, 'w') as z:
                pass
            meta = extract_ota_metadata(path)
            assert meta == {}
        finally:
            os.unlink(path)

    def test_corrupted_zip(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as f:
            f.write(b'not a zip file at all')
            path = f.name
        try:
            meta = extract_ota_metadata(path)
            assert meta == {}
        finally:
            os.unlink(path)

    def test_metadata_priority_over_payload(self):
        """metadata file should not be overwritten by payload_properties."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as f:
            path = f.name
        try:
            with zipfile.ZipFile(path, 'w') as z:
                z.writestr('META-INF/com/android/metadata', 'pre-device=CPH2581')
                z.writestr('payload_properties.txt', 'pre-device=OVERRIDE')
            
            meta = extract_ota_metadata(path)
            assert meta['pre-device'] == 'CPH2581'  # original preserved
        finally:
            os.unlink(path)
