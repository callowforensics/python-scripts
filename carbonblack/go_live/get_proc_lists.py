#!/usr/bin/env python3
from cb_framework import CbGoLive
import cb_logger
import sys
import os

if __name__ == "__main__":
    # Check that the user has enter enough args.
    if len(sys.argv) != 5:
        print("Usage: cb_api_key cb_server_url output_dir hosts_to_get_procs_from")
        print("\nExample:")
        print("-" * 50)
        print(r"abcdefghijklmnopqrstuvwxyz https://123.456.789.1 c:\output hosts_to_get_procs_from.txt")
        sys.exit()

    cb_api = sys.argv[1]
    cb_url = sys.argv[2]
    output_dir = sys.argv[3]
    hosts = sys.argv[4]

    with open(hosts, "r") as f:
        hosts_to_get_from = [line.strip() for line in f if line != "\n"]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cb_logger.logger(output_dir)

    triage = CbGoLive(cb_api_key=cb_api, cb_server_url=cb_url, cb_output_path=output_dir)
    triage.get_sensor_details()
    online = triage.online_sensors

    for host in hosts_to_get_from:
        for sensor in online:
            if sensor["computer_name"].lower() == host.lower():
                sensor_id, host = sensor["id"], sensor["computer_name"]
                triage.setup_go_live_session(sensor_id=sensor_id, host=host)
                if triage.go_live_session_status:
                    proc = triage.get_running_processes()
                    if proc:
                        triage.create_running_process_report(process_list=proc)
                    triage.close_session()
