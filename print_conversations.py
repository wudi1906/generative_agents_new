import os
import sys
import json
import re


def get_unique_conversations(simulation_name):
    
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
     



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the simulation name as a command line argument.")
        sys.exit(1)

    simulation_name = sys.argv[1]
    '''
    unique_conversations = get_unique_conversations(simulation_name)
    print(json.dumps(unique_conversations, indent=2))
    '''
    get_unique_conversations(simulation_name)
