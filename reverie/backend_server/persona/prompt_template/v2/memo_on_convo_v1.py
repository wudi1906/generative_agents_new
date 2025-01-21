# memo_on_convo_v1.py

import traceback

from utils import debug
from ..common import openai_config, ConvoTakeaways
from ..gpt_structure import generate_prompt, safe_generate_structured_response
from ..print_prompt import print_run_prompts

# Variables:
# !<INPUT 0>! -- All convo utterances
# !<INPUT 1>! -- persona name
# !<INPUT 2>! -- persona name
# !<INPUT 3>! -- persona name

template = """
[Conversation]
!<INPUT 0>!

Write down if there is anything from the conversation that !<INPUT 1>! might have found interesting from !<INPUT 2>!'s perspective, in a full sentence.

"!<INPUT 3>!
"""


def run_gpt_prompt_memo_on_convo_v1(persona, all_utt, test_input=None, verbose=False):
  def create_prompt_input(persona, all_utt, test_input=None):
    prompt_input = [
      all_utt,
      persona.scratch.name,
      persona.scratch.name,
      persona.scratch.name,
    ]
    return prompt_input

  def __func_clean_up(gpt_response, prompt=""):
    return gpt_response.split('"')[0].strip()

  def __func_validate(gpt_response, prompt=""):
    try:
      __func_clean_up(gpt_response, prompt)
      return True
    except:
      traceback.print_exc()
      return False

  def get_fail_safe():
    return "..."

  gpt_param = {
    "engine": openai_config["model"],
    "max_tokens": 300,
    "temperature": 0,
    "top_p": 1,
    "stream": False,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": None,
  }
  prompt_template = "persona/prompt_template/v2/memo_on_convo_v1.py"
  prompt_input = create_prompt_input(persona, all_utt)
  prompt = generate_prompt(prompt_input, prompt_template_str=template)

  fail_safe = get_fail_safe()
  output = safe_generate_structured_response(
    prompt,
    gpt_param,
    ConvoTakeaways,
    5,
    fail_safe,
    __func_validate,
    __func_clean_up,
  )

  if debug or verbose:
    print_run_prompts(prompt_template, persona, gpt_param, prompt_input, prompt, output)

  return output, [output, prompt, gpt_param, prompt_input, fail_safe]
