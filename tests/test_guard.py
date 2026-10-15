"""Subprocess tests: no fixture code is executed by the guard."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'byte_literal_guard.py'


class GuardTests(unittest.TestCase):
    def run_guard(self, files=None, arguments=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, content in (files or {}).items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content.encode('utf-8') if isinstance(content, str) else content)
            args = arguments if arguments is not None else [str(root)]
            return subprocess.run([sys.executable, '-B', str(SCRIPT), *args], capture_output=True, text=True)

    def test_bad_literals(self):
        samples = ['b"ż"', "b'ą'", 'B"é"', 'br"ł"', 'rb"ę"', 'b"""line\nż"""', "b'''ó'''", 'b"🐿"', '(b"a" b"ż")']
        for value in samples:
            with self.subTest(value=value):
                result = self.run_guard({'x.py': 'x = ' + value + '\n'})
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn('non-ascii-byte-literal:', result.stderr)

    def test_allowed_literals(self):
        samples = ['b"abc"', r'b"\xff"', r'b"\xc5\xbc"', '"żółw"', 'r"ż"', 'u"ą"', 'f"ż{1}"', '# b"ż"\nx = 1', '"b\\\"ż\\\""']
        for value in samples:
            with self.subTest(value=value):
                result = self.run_guard({'x.py': value + '\n'})
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_location(self):
        result = self.run_guard({'x.py': '# comment\nx = b"ż"\n'})
        self.assertIn('x.py:2', result.stderr)

    def test_nested(self):
        self.assertEqual(self.run_guard({'src/x.py': 'b"ż"'}).returncode, 1)

    def test_skips_cache_and_environments(self):
        files = {'ok.py': 'b"ok"', '.git/x.py': 'b"ż"', '.venv/x.py': 'b"ż"', '__pycache__/x.py': 'b"ż"'}
        result = self.run_guard(files)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('(1 Python files)', result.stdout)

    def test_non_python_ignored(self):
        result = self.run_guard({'ok.py': 'b"ok"', 'notes.txt': 'b"ż"'})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_input(self):
        result = self.run_guard(arguments=['/this-path-does-not-exist-byte-literal-guard'])
        self.assertEqual(result.returncode, 2)

    def test_no_python_files(self):
        self.assertEqual(self.run_guard({'readme.txt': 'hello'}).returncode, 2)

    def test_tokenization_error(self):
        self.assertEqual(self.run_guard({'x.py': 'x = """unfinished'}).returncode, 2)

    def test_encoding_cookie(self):
        content = '# coding: latin-1\nx = b"é"\n'.encode('latin-1')
        self.assertEqual(self.run_guard({'x.py': content}).returncode, 1)

    def test_utf8_bom(self):
        self.assertEqual(self.run_guard({'x.py': b'\xef\xbb\xbfx = b"ok"\n'}).returncode, 0)

    def test_undecodable(self):
        self.assertEqual(self.run_guard({'x.py': b'x = "\xff"\n'}).returncode, 2)

    def test_does_not_execute_input(self):
        result = self.run_guard({'x.py': 'raise RuntimeError("must not execute")\n'})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_not_a_syntax_validator(self):
        result = self.run_guard({'x.py': 'if True print("syntax error")\n'})
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
