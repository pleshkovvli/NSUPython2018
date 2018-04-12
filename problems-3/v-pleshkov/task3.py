import unittest


def read_lazy(file, chunk_size=512):
    if chunk_size <= 0:
        raise ValueError("Chunk size should be greater than zero")

    if "b" in file.mode:
        empty = b""
    else:
        empty = ""

    for chunk in iter(lambda: file.read(chunk_size), empty):
        for symbol in chunk:
            yield symbol


class TestLazyReading(unittest.TestCase):
    def testText(self):
        for mode in ["r", "r+"]:
            self._test_file("test_file", mode)

    def testBinary(self):
        for mode in ["rb", "r+b", "br", "rb+"]:
            self._test_file("test_file", mode)

    def _test_file(self, filename, mode):
        with open(filename, mode) as file:
            content = file.read()
            file.seek(0)
            self._assert_same_content(content, file)

    def _assert_same_content(self, all_content, file):
        chunk_size = 512
        count = 0
        for symbol in read_lazy(file, chunk_size):
            self.assertEqual(symbol, all_content[count])
            count += 1


if __name__ == "__main__":
    unittest.main()
    