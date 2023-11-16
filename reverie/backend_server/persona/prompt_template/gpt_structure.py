"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: gpt_structure.py
Description: Wrapper functions for calling OpenAI APIs.
"""
import json
import random
import time
from typing import Dict, List
import requests
from utils import *

# ============================================================================
# ################### [Set LLM] ###################
# ============================================================================



def llm(prompt):
  log = open("log.txt", "a")
  log.write(f"Prompt @ {time.time()}: {prompt}\n")
  api_url = "http://<instance-ip>:8000/generate"

  payload = {
      "inputs": [{"role": "user", "content": prompt}], 
      "parameters": {"max_new_tokens": 25, "top_p": 0.9, "temperature": 0.6, "do_sample": True}
  }
  headers = {'Content-Type': 'application/json'}
  response = requests.post(api_url, data=json.dumps(payload), headers=headers)
  response = response.json()
  log.write(f"Response @ {time.time()}: {response}\n")
  log.close()

  return response['text']

def temp_sleep(seconds=0.1):
  time.sleep(seconds)

def ChatGPT_single_request(prompt): 
  temp_sleep()
  try:
    response = llm( prompt)
  except:
    print("Requested tokens exceed context window")
    ### TODO: Add map-reduce or splitter to handle this error.
    prompt = prompt.split(" ")[-1400:]
    prompt = str(' '.join(prompt))
    response = llm(prompt)
    response = response.json()
  return response

# ============================================================================
# #####################[SECTION 1: CHATGPT-3 STRUCTURE] ######################
# ============================================================================

def ChatGPT_request(prompt,parameters): 
  """
  Given a prompt, make a request to LLM server and returns the response. 
  ARGS:
    prompt: a str prompt 
    parameters: optional
  RETURNS: 
    a str of LLM's response. 
  """
  # temp_sleep()
  try:
    response = llm( prompt)
  except:
    print("Requested tokens exceed context window")
    ### TODO: Add map-reduce or splitter to handle this error.
    prompt = prompt.split(" ")[-1400:]
    prompt = str(' '.join(prompt))
    response = llm( prompt)
  return response

def ChatGPT_safe_generate_response(prompt, 
                                   example_output,
                                   special_instruction,
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  # prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
  prompt = '"""\n' + prompt + '\n"""\n'
  prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  prompt += "Example output json:\n"
  prompt += '{"output": "' + str(example_output) + '"}'

  if verbose: 
    print ("LLM PROMPT")
    print (prompt)

  for i in range(repeat): 

    try: 
      curr_gpt_response = ChatGPT_request(prompt).strip()
      end_index = curr_gpt_response.rfind('}') + 1
      curr_gpt_response = curr_gpt_response[:end_index]
      curr_gpt_response = json.loads(curr_gpt_response)["output"]

      # print ("---ashdfaf")
      # print (curr_gpt_response)
      # print ("000asdfhia")
      
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      
      if verbose: 
        print ("---- repeat count: \n", i, curr_gpt_response)
        print (curr_gpt_response)
        print ("~~~~")

    except: 
      pass

  return False


def ChatGPT_safe_generate_response_OLD(prompt, 
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  if verbose: 
    print ("CHAT GPT PROMPT")
    print (prompt)

  for i in range(repeat): 
    try: 
      curr_gpt_response = ChatGPT_request(prompt).strip()
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      if verbose: 
        print (f"---- repeat count: {i}")
        print (curr_gpt_response)
        print ("~~~~")

    except: 
      pass
  print ("FAIL SAFE TRIGGERED") 
  return fail_safe_response


# ============================================================================
# ###################[SECTION 2: ORIGINAL GPT-3 STRUCTURE] ###################
# ============================================================================

def GPT_request(prompt,parameters): 
  """
  Given a prompt, make a request to LLM server and returns the response. 
  ARGS:
    prompt: a str prompt 
    parameters: optional 
  RETURNS: 
    a str of LLM's response. 
  """
  # temp_sleep()
  # try:
  response = llm(prompt)
  # except:
  #   print("Requested tokens exceed context window")
  #   ### TODO: Add map-reduce or splitter to handle this error.
  #   prompt = prompt.split(" ")[-1400:]
  #   prompt = str(' '.join(prompt))
  #   response = llm( prompt)
  return response

def generate_prompt(curr_input, prompt_lib_file): 
  """
  Takes in the current input (e.g. comment that you want to classifiy) and 
  the path to a prompt file. The prompt file contains the raw str prompt that
  will be used, which contains the following substr: !<INPUT>! -- this 
  function replaces this substr with the actual curr_input to produce the 
  final promopt that will be sent to the GPT3 server. 
  ARGS:
    curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                INPUT, THIS CAN BE A LIST.)
    prompt_lib_file: the path to the promopt file. 
  RETURNS: 
    a str prompt that will be sent to OpenAI's GPT server.  
  """
  if type(curr_input) == type("string"): 
    curr_input = [curr_input]
  curr_input = [str(i) for i in curr_input]

  f = open(prompt_lib_file, "r")
  prompt = f.read()
  f.close()
  for count, i in enumerate(curr_input):   
    prompt = prompt.replace(f"!<INPUT {count}>!", i)
  if "<commentblockmarker>###</commentblockmarker>" in prompt: 
    prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
  return prompt


def safe_generate_response(prompt, 
                           gpt_parameter,
                           repeat=1,
                           fail_safe_response="error",
                           func_validate=None,
                           func_clean_up=None,
                           verbose=False): 
  print(f"Safe generate response prompt: {prompt}")
  if verbose: 
    print (prompt)

  for i in range(repeat): 
    curr_gpt_response = GPT_request(prompt, gpt_parameter)
    print(f"Func validate: {func_validate(curr_gpt_response, prompt=prompt)}")
    if func_validate(curr_gpt_response, prompt=prompt): 
      return func_clean_up(curr_gpt_response, prompt=prompt)
    if verbose: 
      print ("---- repeat count: ", i, "response: ", curr_gpt_response)
      print ("~~~~")
  return "Hotdog"

def get_embedding(documents):
  api_url = "http://<instance-ip>:8000/embed"
  payload = {"documents": documents}
  response = requests.post(api_url, json=payload)
  response = response.json()
  return response
  
