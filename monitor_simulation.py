import os
import time
import json
import glob

frontend_path = "environment/frontend_server"

# Extract curr_sim_code from JSON file
with open(f"{frontend_path}/temp_storage/curr_sim_code.json", "r") as f:
    data = json.load(f)
    curr_sim_code = data["sim_code"]

movement_path = f"{frontend_path}/storage/{curr_sim_code}/movement"
length = len(movement_path) + 1
last_file = None

while True:
    list_of_files = glob.glob(f"{movement_path}/*.json")
    latest_file = sorted(list_of_files, key=lambda s: int(s[length:-5]))[-1]

    if latest_file != last_file:
        os.system("clear")
        with open(latest_file, "r") as f:
            print(f.read())
            print(latest_file)

        last_file = latest_file

    time.sleep(0.2)
