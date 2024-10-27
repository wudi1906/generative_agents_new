import glob
import os
import glob
import os
import sys
import json
import re

def get_unique_conversations(simulation_name):
<<<<<<< HEAD
    
    step_folder = f"environment/frontend_server/storage/base_search_and_rescue/{simulation_name}/movement"
    print(os.listdir())
    # Iterate over all files in the simulation folder
    for filename in os.listdir(step_folder):
        filepath = os.path.join(step_folder, filename)
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
                for k, v in data.items():
                    print(k)
                    if(k=='persona'):
                        for key, value in v.items():
                            print(f'   {key}')
                            for attribute, val in value.items():
                                if attribute!='chat' or attribute=='chat' and val is None:
                                    print(f'      {attribute}: {val}')
                                else:
                                    print(f'      {attribute}:')
                                    for convo in val: 
                                        print(f'         {convo[0]}: {convo[1]}')
                                        
                    else:
                        for key,value in v.items():
                            print(f'   {key}: {value}')
                    print('\n')
        except json.JSONDecodeError:
            print("Failed to decode JSON. Please check the file format.")
        except Exception as e:
            print(f"An error occurred: {e}")
     

=======
    step_folder = "environment/frontend_server/storage"
    
    # Use glob to find all files that start with the simulation_name
    search_pattern = os.path.join(step_folder, f"{simulation_name}*/movement/*")
    filepaths = glob.glob(search_pattern)

    observed_conversations = set()
    file_contents = []

    # Iterate over all matching files
    for filepath in filepaths:
        with open(filepath, "r") as file:
            data = json.load(file)
            personas = data.get("persona", {})

            # Loop over all personas except one, since conversations are always
            # between two people
            for name in list(personas.keys())[:-1]:
                persona = personas[name]
                chat = persona.get("chat")

                if chat:
                    chat_string = str(chat)

                    # Add unique conversations
                    if chat_string not in observed_conversations:
                        observed_conversations.add(chat_string)
                        file_contents.append(data)
                        break

    return file_contents
>>>>>>> origin/henry-dev-rebase

def write_conversations_to_file(conversations, simulation_name):
   output_directory = "logs/conversations"
   if not os.path.exists(output_directory):
        os.makedirs(output_directory)
   output_filename = f"{simulation_name}_highlights.json"
   full_path = os.path.join(output_directory, output_filename);
   with open(full_path, "w") as file:
        for conversation in conversations:
            json.dump(conversation, file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the simulation name as a command line argument.")
        sys.exit(1)

    simulation_name = sys.argv[1]
    '''
    unique_conversations = get_unique_conversations(simulation_name)
<<<<<<< HEAD
    print(json.dumps(unique_conversations, indent=2))
    '''
    get_unique_conversations(simulation_name)
=======
    
    if unique_conversations:
        write_conversations_to_file(unique_conversations, simulation_name)
        print(f"Unique conversations written to {simulation_name}_highlights.txt")
    else:
        print("No unique conversations found.")
>>>>>>> origin/henry-dev-rebase
