import unittest

from unittest.mock import patch, MagicMock

from parsers.image_parser import ImgParser


class TestImageParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = ImgParser(
            url="https://example.com", directory="/path/to/directory"
        )

    @patch("parsers.media_parser.MediaParser.download")
    @patch("parsers.media_parser.MediaParser.fetch")
    def test_parse(self, mock_fetch, mock_download):
        mock_fetch.return_value = [
            MagicMock(get=lambda attr: "image1.jpg"),
            MagicMock(get=lambda attr: "image2.jpg"),
        ]
        self.parser.parse()
        self.assertEqual(mock_fetch.call_count, 1)
        self.assertEqual(mock_download.call_count, 2)


if __name__ == "__main__":
    unittest.main()