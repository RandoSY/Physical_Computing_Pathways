import csv
import struct
import tempfile
import unittest
from pathlib import Path
from host.protocol import FIELDS, Sample, decode_line, decode_packet
from host.report import render

class ProtocolTests(unittest.TestCase):
    def test_binary_and_serial_agree(self):
        expected = Sample(65535, 0xffffffff, 32768, 1, 0, 1, 1050)
        self.assertEqual(decode_line("65535,4294967295,32768,1,0,1,1050\r\n"), expected)
        self.assertEqual(decode_packet(struct.pack("<BBHIHH", 1, 5, 65535,
                         0xffffffff, 32768, 1050)), expected)

    def test_invalid_serial(self):
        for line in ("", "booting", "0,0,0,0,0,1", "0,0,0,0,0,1,100,9",
                     "-1,0,0,0,0,1,100", "0,0,65536,0,0,1,100",
                     "0,0,0,2,0,1,100", "0,0,0,0,0,1,99",
                     "0,0,0,0,0,1,2001", "0,0,1.5,0,0,1,100"):
            with self.subTest(line=line), self.assertRaises(ValueError): decode_line(line)

    def test_invalid_packets(self):
        for packet in (b"", bytes(13), struct.pack("<BBHIHH", 2, 0, 0, 0, 0, 100),
                       struct.pack("<BBHIHH", 1, 8, 0, 0, 0, 100)):
            with self.assertRaises(ValueError): decode_packet(packet)

    def test_report_wrap_and_gaps(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trace.csv"
            with path.open("w", newline="") as file:
                writer = csv.writer(file); writer.writerow(FIELDS)
                for seq in (65535, 0, 2): writer.writerow((seq, 0, 1234, 0, 0, 1, 100))
            report = render(path)
            self.assertIn("sequence discontinuities: 1", report)
            self.assertIn("3 samples", report)

    def test_empty_report_is_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.csv"
            path.write_text(",".join(FIELDS) + "\n")
            with self.assertRaisesRegex(ValueError, "no samples"): render(path)
