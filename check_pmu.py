#!/usr/bin/env python3

import sys
import os
import json
import re

if __name__ == "__main__":
    linux_perf_dir = sys.argv[1]
    core_event_table = sys.argv[2]
    exist_events = set()
    core_events = set()
    with open(core_event_table, "r") as f:
        lines = f.readlines()
        for line in lines:
            core_events.add(line.strip())
    for pmu_json in os.listdir(linux_perf_dir):
        json_path = os.path.join(linux_perf_dir, pmu_json)
        with open(json_path, "r") as f:
            json_data = json.loads(f.read())
            for event in json_data:
                if "MetricExpr" in event:
                    # Allow 1-3 since we have Level 1, Level 2, and Level 3 cache events
                    events = re.findall(r"([A-Z_1-3]{3,})", event["MetricExpr"])
                    for e in events:
                        if len(e) < 3:
                            print("Invalid event:", e, file=sys.stderr)
                            exit(1)
                        exist_events.add(e)
                elif "ArchStdEvent" in event:
                    exist_events.add(event["ArchStdEvent"])
                else:
                    print("Unknown event type", event)
    print("Events missing in json files:")
    for event in sorted(core_events):
        if event not in exist_events:
            print(event)
    print("Events missing in core_event_table:")
    for event in sorted(exist_events):
        if event not in core_events:
            print(event)