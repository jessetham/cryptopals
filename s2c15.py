import unittest
from util import padding

class TestCase(unittest.TestCase):
    def test_pkcs7Validation(self):
        b1 = b"ICE ICE BABY"
        p1 = padding.pkcs7Pad(b1)
        self.assertEqual(padding.pkcs7Strip(p1), b1)

        # Invalid pad
        p2 = b"ICE ICE BABY\x01\x02\x03\x04"
        with self.assertRaises(padding.BadPaddingException):
            padding.pkcs7Strip(p2)

if __name__ == "__main__":
    unittest.main()