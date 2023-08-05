import sys
import os
from scyllaso import util


def cli():
    if len(sys.argv) == 1:
        print("No data directory")
        exit(1)

    old_wd = os.getcwd()
    data_dir = sys.argv[1]

    if not os.path.isabs(data_dir):
        data_dir = os.path.join(old_wd, data_dir)

    if not os.path.exists(data_dir):
        print(f"[{data_dir}] does not exist!")
        exit(1)

    if not os.path.isdir(data_dir):
        print(f"[{data_dir}] is not a directory!")
        exit(1)

    scylla_monitoring_path = os.environ['SCYLLA_MONITORING']

    old_wd = os.getcwd()
    os.chdir(scylla_monitoring_path)

    util.log_important("Killing Scylla Monitoring: starting")
    os.system("./kill-all.sh")
    util.log_important("Killing Scylla Monitoring: done")

    util.log_important("Starting Scylla Monitoring: started")
    os.system(f"./start-all.sh -d {data_dir} -s prometheus/scylla_servers.example.yml")
    util.log_important("Starting Scylla Monitoring: done")

    os.chdir(old_wd)
