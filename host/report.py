"""Create an offline HTML instrument trace from a capture CSV."""
import argparse
import csv
import html
from pathlib import Path
from .protocol import FIELDS, Sample

def render(path):
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("CSV columns do not match Pathways protocol")
        samples = [Sample(*(int(row[key]) for key in FIELDS)) for row in reader]
    if not samples:
        raise ValueError("Capture contains no samples")
    # Plot sample index: avoids implying wall-time continuity across resets/wraps.
    width = 940
    count = max(1, len(samples) - 1)
    points = " ".join("{:.2f},{:.2f}".format(30 + i * width / count,
                    240 - s.input_u16 * 200 / 65535) for i, s in enumerate(samples))
    gaps = sum((b.seq - a.seq) % 65536 != 1 for a, b in zip(samples, samples[1:]))
    rows = "".join("<tr>" + "".join("<td>{}</td>".format(v) for v in s.row()) + "</tr>"
                   for s in samples[-25:])
    headers = "".join("<th>{}</th>".format(f) for f in FIELDS)
    return '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Physical Computing Pathways | Instrument trace</title>
<style>body{font:17px system-ui;background:#edf3f8;color:#19334a;max-width:1100px;margin:auto;padding:32px}
h1{font-size:36px;margin-bottom:8px}header{border-top:7px solid #008f87}section{background:white;padding:24px;border-radius:16px;margin:24px 0}
svg{width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:14px}td,th{text-align:right;padding:7px;border-bottom:1px solid #dde5eb}.scroll{overflow:auto}small{color:#496378}</style>
<header><p>GCBASIC → Arduino / C++ → MicroPython + BLE</p><h1>Physical Computing Pathways</h1><p>Virtual instrument · recorded input trace</p></header>
<section><b>''' + str(len(samples)) + ''' samples</b> · sequence discontinuities: ''' + str(gaps) + '''<p>Source: ''' + html.escape(Path(path).name) + '''</p>
<svg viewBox="0 0 1000 280" role="img" aria-label="Normalized input versus sample index">
<path d="M30 40V240H970" fill="none" stroke="#a8bdcd"/>
<text x="35" y="28" fill="#496378">65535</text><text x="35" y="265" fill="#496378">0 · sample index →</text>
<polyline fill="none" stroke="#008f87" stroke-width="3" points="''' + points + '''"/></svg>
<small>Normalized ADC counts, not calibrated volts. Horizontal spacing is sample index. Discontinuities may indicate loss, duplicates, reordering, or a device reset.</small></section>
<section><h2>Most recent 25 samples</h2><div class="scroll"><table><tr>''' + headers + '''</tr>''' + rows + '''</table></div></section></html>'''

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv")
    parser.add_argument("--output", default="trace.html")
    args = parser.parse_args()
    try:
        result = render(args.csv)
        Path(args.output).write_text(result, encoding="utf-8")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, str(exc) + "\n")
    print("Created", args.output)

if __name__ == "__main__":
    main()
