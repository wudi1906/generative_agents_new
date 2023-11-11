"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: gpt_structure.py
Description: Wrapper functions for calling OpenAI APIs.
"""
import time 
import json
from pathlib import Path
from openai import AzureOpenAI, OpenAI

from utils import *
from openai_cost_logger import DEFAULT_LOG_PATH
from persona.prompt_template.openai_logger_singleton import OpenAICostLogger_Singleton

config_path = Path("../../openai_config.json")
with open(config_path, "r") as f:
    openai_config = json.load(f) 
import boto3
import random
from typing import Dict, List

# from langchain.llms import Ollama
# from langchain.llms import OpenAI
# from langchain.llms import LlamaCpp
# from langchain.llms import GPT4All
# from langchain.chat_models import ChatAnthropic
# from langchain.embeddings import GPT4AllEmbeddings
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.llms import HuggingFacePipeline


# ============================================================================
# ################### [Set LLM] ###################
# ============================================================================

### **** OpenAI **** 
'''
llm = OpenAI(temperature=0,model_name="gpt-3.5-turbo-16k")
'''

### **** Anthropic **** 
'''
llm = ChatAnthropic(model_name="claude-2", temperature=0)
'''

### *** Llama.cpp (Llama2-13b) ***
'''
n_gpu_layers = 1  # Metal set to 1 is enough.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
model_path="/Users/rlm/Desktop/Code/llama.cpp/llama-2-13b-chat.ggmlv3.q4_0.bin"
llm = LlamaCpp(
    model_path=model_path,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    n_ctx=4096,
    f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
    callback_manager=callback_manager,
    verbose=True,
)
''' 

### *** GPT4Alll (nous-hermes-13b) *** 
''' 
model_path = "/Users/rlm/Desktop/Code/gpt4all/models/nous-hermes-13b.ggmlv3.q4_0.bin"
llm = GPT4All(
    model=model_path
)
'''

### *** Ollama (Vicuna-13b-16k) *** 
''' 
llm = Ollama(base_url="http://localhost:11434",
              model="vicuna:13b-v1.5-16k-q4_0",
              callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]))
'''

### *** Ollama (Llama2-13b) *** 
'''
llm = Ollama(base_url="http://localhost:11434",
              model="llama2:13b",
              callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]))
'''

### *** Hugging Face Transformers ***
'''
llm = pipeline("text-generation", model="meta-llama/Llama-2-13b-chat-hf", device=0, token=huggingface_token)
# llm.tokenizer.pad_token_id = llm.model.config.eos_token_id
'''

### *** SageMaker Jumpstart ***


# def llm(prompt):
#   payload =  {
#     "inputs": prompt, 
#     "parameters": {"max_new_tokens": 256, "top_p": 0.9, "temperature": 0.6}
#   }
#   endpoint_name = 'jumpstart-dft-meta-textgeneration-llama-codellama-7b'
#   client = boto3.client("sagemaker-runtime")
#   response = client.invoke_endpoint(
#     EndpointName=endpoint_name,
#     ContentType="application/json",
#     Body=json.dumps(payload),
#     CustomAttributes="accept_eula=true",
#   )
#   response = response["Body"].read().decode("utf8")
#   response = json.loads(response)
#   return response["generated_text"]

def setup_client(type: str, config: dict):
  """Setup the OpenAI client.

  Args:
      type (str): the type of client. Either "azure" or "openai".
      config (dict): the configuration for the client.

  Raises:
      ValueError: if the client is invalid.

  Returns:
      The client object created, either AzureOpenAI or OpenAI.
  """
  if type == "azure":
    client = AzureOpenAI(
        azure_endpoint=config["endpoint"],
        api_key=config["key"],
        api_version=config["api-version"],
    )
  elif type == "openai":
    client = OpenAI(
        api_key=config["key"],
    )
  else:
    raise ValueError("Invalid client")
  return client

if openai_config["client"] == "azure":
  client = setup_client("azure", {
      "endpoint": openai_config["model-endpoint"],
      "key": openai_config["model-key"],
      "api-version": openai_config["model-api-version"],
  })
elif openai_config["client"] == "openai":
  client = setup_client("openai", { "key": openai_config["model-key"] })

if openai_config["embeddings-client"] == "azure":  
  embeddings_client = setup_client("azure", {
      "endpoint": openai_config["embeddings-endpoint"],
      "key": openai_config["embeddings-key"],
      "api-version": openai_config["embeddings-api-version"],
  })
elif openai_config["embeddings-client"] == "openai":
  embeddings_client = setup_client("openai", { "key": openai_config["embeddings-key"] })
else:
  raise ValueError("Invalid embeddings client")

cost_logger = OpenAICostLogger_Singleton(
  experiment_name = openai_config["experiment-name"],
  log_folder = DEFAULT_LOG_PATH,
  cost_upperbound = openai_config["cost-upperbound"]
)

def ChatGPT_single_request(prompt): 
  temp_sleep()

  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-1106", 
    messages=[{"role": "user", "content": prompt}]
  )
  return completion["choices"][0]["message"]["content"]

  # try:
  #   response = llm(prompt)
  # except:
  #   print("Requested tokens exceed context window")
  #   ### TODO: Add map-reduce or splitter to handle this error.
  #   prompt = prompt.split(" ")[-1400:]
  #   prompt = str(' '.join(prompt))
  #   response = llm(prompt)
  # return response


def temp_sleep(seconds=0.1):
  time.sleep(seconds)


def ChatGPT_single_request(prompt): 
  temp_sleep()
  completion = client.chat.completions.create(
    model=openai_config["model"],
    messages=[{"role": "user", "content": prompt}]
  )
  cost_logger.update_cost(completion, input_cost=openai_config["model-costs"]["input"], output_cost=openai_config["model-costs"]["output"])
  return completion.choices[0].message.content


def ChatGPT_request(prompt, parameters): 
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
    completion = client.chat.completions.create(
    model=openai_config["model"],
    messages=[{"role": "user", "content": prompt}]
    )
    cost_logger.update_cost(completion, input_cost=openai_config["model-costs"]["input"], output_cost=openai_config["model-costs"]["output"])
    return completion.choices[0].message.content
  
  except Exception as e: 
    print(f"Error: {e}")
    return "ChatGPT ERROR"

  # try:
  #   response = llm(prompt)
  # except:
  #   print("Requested tokens exceed context window")
  #   ### TODO: Add map-reduce or splitter to handle this error.
  #   prompt = prompt.split(" ")[-1400:]
  #   prompt = str(' '.join(prompt))
  #   response = llm(prompt)
  # return response


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

      if verbose: 
        print ("---- repeat count:", i)
        print ("~~~~ curr_gpt_response:")
        print (curr_gpt_response)
        print ("~~~~")
      
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)

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
def GPT_request(prompt, gpt_parameter): 
  """
  Given a prompt, make a request to LLM server and returns the response. 
  ARGS:
    prompt: a str prompt 
    parameters: optional 
  RETURNS: 
    a str of LLM's response. 
  """
  temp_sleep()
  try: 
    messages = [{
      "role": "system", "content": prompt
    }]
    response = client.chat.completions.create(
                model=gpt_parameter["engine"],
                messages=messages,
                temperature=gpt_parameter["temperature"],
                max_tokens=gpt_parameter["max_tokens"],
                top_p=gpt_parameter["top_p"],
                frequency_penalty=gpt_parameter["frequency_penalty"],
                presence_penalty=gpt_parameter["presence_penalty"],
                stream=gpt_parameter["stream"],
                stop=gpt_parameter["stop"],)
    cost_logger.update_cost(response=response, input_cost=openai_config["model-costs"]["input"], output_cost=openai_config["model-costs"]["output"])
    return response.choices[0].message.content
  except Exception as e:
    print(f"Error: {e}")
    return "TOKEN LIMIT EXCEEDED"

  # temp_sleep()
  # try:
  #   response = llm(prompt)
  # except:
  #   print("Requested tokens exceed context window")
  #   ### TODO: Add map-reduce or splitter to handle this error.
  #   prompt = prompt.split(" ")[-1400:]
  #   prompt = str(' '.join(prompt))
  #   response = llm(prompt)
  # return response

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
  return prompt.strip()


def safe_generate_response(prompt, 
                           gpt_parameter,
                           repeat=1,
                           fail_safe_response="error",
                           func_validate=None,
                           func_clean_up=None,
                           verbose=False): 
  if verbose: 
    print (prompt)

  for i in range(repeat): 
    curr_gpt_response = GPT_request(prompt, gpt_parameter)
    try:
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      if verbose: 
        print ("---- repeat count: ", i, curr_gpt_response)
        print (curr_gpt_response)
        print ("~~~~")
    except:
      pass
  return fail_safe_response


def get_embedding(text, model=openai_config["embeddings"]):
  text = text.replace("\n", " ")
  if not text: 
    text = "this is blank"
  response = embeddings_client.embeddings.create(input=[text], model=model)
  cost_logger.update_cost(response=response, input_cost=openai_config["embeddings-costs"]["input"], output_cost=openai_config["embeddings-costs"]["output"])
  return response.data[0].embedding

  # endpoint_name = 'jumpstart-dft-hf-textembedding-gpt-j-6b-fp16'
  # client = boto3.client('runtime.sagemaker')
  # payload = {"text_inputs": [text]}
  # query_response = client.invoke_endpoint(EndpointName=endpoint_name, ContentType='application/json', Body=json.dumps(payload).encode('utf-8'))
  # model_predictions = json.loads(query_response['Body'].read())
  # return model_predictions['embedding'][0]


if __name__ == '__main__':
  gpt_parameter = {"engine": openai_config["model"], "max_tokens": 50, 
                   "temperature": 0, "top_p": 1, "stream": False,
                   "frequency_penalty": 0, "presence_penalty": 0, 
                   "stop": ['"']}
  curr_input = ["driving to a friend's house"]
  prompt_lib_file = "prompt_template/v1/test_prompt_July5.txt"
  prompt = generate_prompt(curr_input, prompt_lib_file)

  def __func_validate(gpt_response): 
    if len(gpt_response.strip()) <= 1:
      return False
    if len(gpt_response.strip().split(" ")) > 1: 
      return False
    return True
  def __func_clean_up(gpt_response):
    cleaned_response = gpt_response.strip()
    return cleaned_response

  output = safe_generate_response(prompt, 
                                 gpt_parameter,
                                 5,
                                 "rest",
                                 __func_validate,
                                 __func_clean_up,
                                 True)

  print (output)


















