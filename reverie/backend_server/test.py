"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: gpt_structure.py
Description: Wrapper functions for calling OpenAI APIs.
"""
import json
import random
from openai import OpenAI

client = OpenAI(api_key=openai_api_key)
import time 

from utils import *

def ChatGPT_request(prompt): 
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response. 
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of  
                   the parameter and the values indicating the parameter 
                   values.   
  RETURNS: 
    a str of GPT-3's response. 
  """
  # temp_sleep()
  try: 
    completion = client.chat.completions.create(model="gpt-4-0125-preview", 
    messages=[{"role": "user", "content": prompt}])
    return completion.choices[0].message.content
  
  except: 
    print ("ChatGPT ERROR")
    return "ChatGPT ERROR"

prompt = """
---
Character 1: Maria Lopez is playing hide-and-seek and hides all over Smallville. She is hiding in the game.
Character 2: Klaus Mueller is playing the hide-and-seek and seeks for the hiders all over Smallville. He is the seeker in the game and is best in the world. 
Character 5: Isabella Rodriguez is playing hide-and-seek and hides all over Smallville. She is hiding in the game.
Past Context: 
Hide-and-Seek Game Rules
*Important for the game*:
The seekers and hiders must not converse with each other. NEVER do this! 
If the seeker interacts anyway with the hiders that would mean that they have been found. 
If the hidder is in the near vicinity to the seeker, the hider has been found. 
Once the hiders have found a spot to hide, they must remain there for the rest of the game, unless they have been found. 

Counting: The seeker covers their eyes at the home base, Johnson Parks Big Oak Tree, and counts to number 50 with their eyes closed, giving hiders time to hide around Smallville away from the seeker 

Hiding: While the seeker is counting, the other players scatter and hide around the Smallville area. Hiders must find a spot where they cannot be seen but still within Smallville.

Seeking: Once the counting is done, the seeker shouts "Ready or not, here I come!" and starts looking for the hiders without returning to the home base, Johnson Parks Big Oak Tree, to peek.

The Chase: When a hider is spotted, the seeker can call out their name and hiding spot. The hider then has to race back to the home base before being tagged by the seeker. If the seeker tags the hider before they reach home base, the hider becomes "caught. and will have to go to Cafe in Smallville where they will remain there stil and not move. 

Safe Calls: If a hider reaches the home base without being tagged by the seeker, they shout "Safe!" and will remain there for the rest of the round and are free from being caught. They cannot be sought after again for this round. 

Winning the Game: The game continues until all hiders are found and caught or return safely to the home base. The time constrain is 7 minutes games. The first person caught or the last to return becomes the next round's seeker. 


Current Context: Maria Lopez is hiding somwhere in Johnson Park when Maria Lopez saw Klaus Mueller in the middle of the park.
Maria Lopez is thinking of staying hidden so Klaus Mueller will not see her.
Current Location: Johnson Park 

(This is what is in Maria Lopez's head: Maria Lopez should remember that Klaus Mueller is the seeker in the game of hide-and-seek and should not talk to him or interact with thim. Beyond this, Maria Lopez doesn't necessarily know anything more about Klaus Mueller) 

(This is what is in Klaus Mueller's head: Klaus Mueller should remember to find Maria Lopez and Isabella Rodriguez. Also, that he should not talk to them and only prioritize winnin the game. Beyond this, Klaus Mueller doesn't necessarily know anything more about Maria Lopez) 

There is no conversation only playing the game by the following words. 


Klaus Mueller: "I see you Maria. You got tagged!"

Maria Lopez: "I lost. You found me."

Klaus Mueller: "Yes, I found you. I won!"


Klaus Mueller: "
---
Output the response to the prompt above in json. The output should be a list of list where the inner lists are in the form of ["<Name>", "<Utterance>"]. Output multiple utterances in ther conversation until the conversation comes to a natural conclusion.
Example output json:
{"output": "[["Jane Doe", "Hi!"], ["John Doe", "Hello there!"] ... ]"}
"""


print (ChatGPT_request(prompt))












