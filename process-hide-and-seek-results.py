import os
import json
import sys


def read_simulation_files(simulation_name):
    plugin_output_path = f"environment/frontend_server/storage/{simulation_name}/plugins/hide-and-seek/output"

    # Check if the directory exists
    if not os.path.isdir(plugin_output_path):
        print(f"The directory {plugin_output_path} does not exist.")
        return

    files = os.listdir(plugin_output_path)
    # Sort by number
    files.sort(key=lambda x: int(x.split("-")[0]))

    # Iterate over all files in the directory
    for filename in files:
        # Check if the file is a JSON file
        if filename.endswith(".json"):
            print(filename)

            # Construct the full file path
            file_path = os.path.join(plugin_output_path, filename)

            # Open the file and load the JSON data
            with open(file_path, "r") as file:
                data = json.load(file)

                game_ended = data[0]["Did a game of hide-and-seek just end?"]
                print(game_ended)

                if game_ended:
                    print(data)
                    print()


# Check if a command-line argument was provided
if len(sys.argv) < 2:
    print("Please provide a simulation name as a command-line argument.")
else:
    # Call the function with the simulation name as argument
    read_simulation_files(sys.argv[1])
