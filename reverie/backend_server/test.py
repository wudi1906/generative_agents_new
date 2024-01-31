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
    completion = client.chat.completions.create(model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": prompt}])
    return completion.choices[0].message.content
  
  except: 
    print ("ChatGPT ERROR")
    return "ChatGPT ERROR"

prompt = """
---
Character 1: Maria Lopez is playing hide-and-seek everyday. She lives at Johnson Park and hides there everyday.
Character 2: Klaus Mueller is playing the hide-and-seek everyday. He is the seeker in the game and is best in the world and loves to play everyday.
Character 3: Abigail Chen is playing hide-and-seek everyday. She lives at Johnson Park and hides there everyday.
Character 4: Adam Smith is playing hide-and-seek everyday. He lives at Johnson Park and hides there everyday.
Character 5: Isabella Rodriguez is playing hide-and-seek everyday. She lives at Johnson Park and hides there everyday.
Past Context: 
1 minutes ago, Maria Lopez, Klaus Mueller, Abigail Chen, Adam Smith, and Isabella Rodriguez were already conversing about setting up the game rules. This context takes place after that conversation.

Current Context: Maria Lopez is hiding at Johson Park when Maria Lopez saw Klaus Mueller in the middle of the park.
Maria Lopez is thinking of staying hidden so Klaus Mueller will not see her.
Current Location: Johnson Park 

(This is what is in Maria Lopez's head: Maria Lopez should remember that Klaus Mueller is the seeker in the game of hide-and-seek. Beyond this, Maria Lopez doesn't necessarily know anything more about Klaus Mueller) 

(This is what is in Klaus Mueller's head: Klaus Mueller should remember to ask Maria Lopez was hiding. Beyond this, Klaus Mueller doesn't necessarily know anything more about Maria Lopez) 

Here is their conversation. 

Maria Lopez: "Hey Klaus! How about a game of hide and seek in Johnson Park? I think it'd be great exercise for our body and mind."

Klaus Mueller: "Hide and seek? Yes, I would love to play. It could be a great way to know who is the best at hide-and-seek. Plus, I've always wanted to explore more of Johnson Park."

Maria Lopez: "Great! I know some excellent hiding spots. But let's set a few ground rules."

Klaus Mueller: "Sounds good! And let's say the big Oak Tree is the home base. Whoever is seeking can start counting there."

Maria Lopez: "Deal! I'll go hide first. Give me a 1 minute head start?"

Klaus Mueller: "1 minute it is! Ready when you are."

Maria Lopez: "Alright, see you soon! And remember, no peeking!"

Klaus Mueller: "
---
Output the response to the prompt above in json. The output should be a list of list where the inner lists are in the form of ["<Name>", "<Utterance>"]. Output multiple utterances in ther conversation until the conversation comes to a natural conclusion.
Example output json:
{"output": "[["Jane Doe", "Hi!"], ["John Doe", "Hello there!"] ... ]"}
"""


print (ChatGPT_request(prompt))












