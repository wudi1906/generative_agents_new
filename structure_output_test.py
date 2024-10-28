from pydantic import BaseModel
from openai import OpenAI
import json

#-------------Enter Pydantic BaseModel for response here----------------
class PromptAgentChat(BaseModel): 
    convo: list[list[str]]

class FocalPt(BaseModel): 
  questions: list[str]

class IntPoignancy(BaseModel): 
  number: int  

class ChatSummarizeRelationship(BaseModel):
  response: str

class InsightGuidance(BaseModel): 
  numberlist: list[str]
  target: str

class ConversationOutput(BaseModel):
    utterance: str
    did_end: bool

class IterativeChat(BaseModel): 
    INPUT0: str 
    INPUT1: str 
    INPUT2: str 
    INPUT3: str
    INPUT4: str 
    INPUT5: str 
    INPUT6: str
    INPUT7: str
    INPUT8: str 
    INPUT9: str
    INPUT10: str
    INPUT11: str
    INPUT12: str
    INPUT13: str
    output: ConversationOutput

    def format_output(self):
        return {
            self.INPUT11: f"{self.INPUT12}'s utterance",
            f"Did the conversation end with {self.INPUT13}'s utterance?": self.output.did_end
        }

#-----------------Input message and object name here------------------
message_input = [
    {"role": "system", "content": 'Variables: \n!<INPUT 0>! -- persona ISS \n!<INPUT 1>! -- persona name \n!<INPUT 2>! -- retrieved memory\n!<INPUT 3>! -- past context \n!<INPUT 4>! -- current location\n!<INPUT 5>! -- current context\n!<INPUT 6>! -- persona name\n!<INPUT 7>! -- target persona name\n!<INPUT 8>! -- curr convo\n!<INPUT 9>! -- persona name\n!<INPUT 10>! -- target persona name\n!<INPUT 11>! -- persona name\n!<INPUT 12>! -- persona name\n!<INPUT 13>! -- persona name\n<commentblockmarker>###</commentblockmarker>\nContext for the task: \nPART 1. \n!<INPUT 0>!\nHere is the memory that is in !<INPUT 1>!''s head: \n!<INPUT 2>! \nPART 2. \nPast Context: \n!<INPUT 3>!\nCurrent Location: !<INPUT 4>!\nCurrent Context: \n!<INPUT 5>!\n!<INPUT 6>! and !<INPUT 7>! are chatting. Here is their conversation so far: \n!<INPUT 8>!'},
    {"role": "user","content": 'Task: Given the above, what should !<INPUT 9>! say to !<INPUT 10>! next in the conversation? And did it end the conversation? \nOutput format: Output a json of the following format: \n{\n"!<INPUT 11>!": "<!<INPUT 12>!''s utterance>",\n"Did the conversation end with !<INPUT 13>!''s utterance?": "<json Boolean>"\n}'}
]
response_format = IterativeChat
#--------------------------------------------------------------------------------
#----------------------------Setting up Client and parameters-------------------
client = OpenAI(api_key="")
with open("openai_config.json", "r") as f:
    openai_config = json.load(f)

gpt_parameter = {
    "engine": openai_config["model"],
    "max_tokens": 1000,  # Increased tokens to allow more conversation
    "temperature": 0.7,
    "top_p": 1,
    "stream": False,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": None
}

#--------------------------------GPT Func Call--------------------------------
completion = client.beta.chat.completions.parse(
    model=gpt_parameter["engine"],
    messages=message_input,
    response_format=response_format,
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
