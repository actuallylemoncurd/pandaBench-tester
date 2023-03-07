#!/usr/bin/env python3
from tools.lib.logreader import LogReader
from tools.lib.route import Route
import csv

f = open('logReaderResults.csv', 'w')
writer = csv.writer(f)
row = ("Source", "Address (dec)", "Data (hex)")
writer.writerow(row)

if __name__ == "__main__":
    route = Route("4cf7a6ad03080c90|2021-09-29--13-46-36")

    for l in route.log_paths():
        lr = LogReader(l)

        for m in lr:
            if m.which() != "can":
                continue

            for c in m.can:
                print(c.src, c.address, c.dat.hex())
                row = (c.src, c.address, c.dat.hex())
                writer.writerow(row)