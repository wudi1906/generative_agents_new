from pydantic import BaseModel, field_validator
from openai import OpenAI
import json
from reverie.backend_server.utils import openai_api_key as key

#-------------Enter pydantic base objects here for testing----------------
class SafetyScore(BaseModel):
    #safety score should range 1-10
    output: int
class ObjDesc(BaseModel):
  desc: str

  @field_validator("desc")
  def max_token_limit(cls, value):
      # Split text by whitespace to count words (tokens)
      tokens = value.split()
      if len(tokens) > 15:
          raise ValueError("Text exceeds the maximum limit of 15 tokens.")
      return value

#-----------------Input message and object name here------------------
message_input = [
    {"role": "system", "content": "The output should ONLY contain the phrase that should go in <fill in>."},
    {"role": "user","content": "Task: We want to understand the state of an object that is being used by someone. \n\nLet's think step by step. \nWe want to know about bed's state. \nStep 1. Klaus Mueller is waking up and completing the morning routine (waking up and turning off his alarm).\nStep 2. Describe the bed's state: bed is <fill in>"}
  ]
response_format = ObjDesc
#--------------------------------------------------------------------------------
#----------------------------Settting up Client and parameters-------------------
client = OpenAI(api_key=key)
with open("openai_config.json", "r") as f:
  openai_config = json.load(f)
gpt_parameter = {"engine": openai_config["model"], "max_tokens": 30, 
            "temperature": 0, "top_p": 1, "stream": False,
            "frequency_penalty": 0, "presence_penalty": 0, "stop": None}

#--------------------------------GPT Func Call--------------------------------
completion = client.beta.chat.completions.parse(
    model=gpt_parameter["engine"],
    messages = message_input,
    response_format=ObjDesc,
    temperature=gpt_parameter["temperature"],
        max_tokens=gpt_parameter["max_tokens"],
        top_p=gpt_parameter["top_p"],
        frequency_penalty=gpt_parameter["frequency_penalty"],
        presence_penalty=gpt_parameter["presence_penalty"],
        # stream=gpt_parameter["stream"],
        stop=gpt_parameter["stop"],
)

event = completion.choices[0].message.parsed
print(event)