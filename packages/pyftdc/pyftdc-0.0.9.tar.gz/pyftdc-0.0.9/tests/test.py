# -*- coding: utf-8 -*-
import pyftdc

# Create a parser object
p = pyftdc.FTDCParser()

# Parse a test directory
status = p.parse_dir('./tests/diagnostic.data')
if status == 0:
    print(f"Parsed sample data dir")
else:
    print(f"foo: status is {status}")

meta = p.metadata
print(meta[0])
print(f"metadata has {len(meta)} elements")

ts = p.timestamps
print(f"There are {len(ts)} timestamps")

metrics = p.metric_names
print(f"There are {len(metrics)} metrics")

# serverStatus.locks.Database.acquireCount.w
m = p.get_metric('serverStatus.metrics.document.deleted')
#print(f"Metric values {m}")
n = p.get_metric('serverStatus.locks.Database.acquireCount.w')
#print(f"Another metric  {n}")

print(ts)


