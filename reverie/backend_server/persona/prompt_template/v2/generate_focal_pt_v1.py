# generate_focal_pt_v1.py

import traceback

from utils import debug
from ..common import openai_config, FocalPoint
from ..gpt_structure import generate_prompt, safe_generate_structured_response
from ..print_prompt import print_run_prompts

# Variables:
# !<INPUT 0>! -- Event/thought statements
# !<INPUT 1>! -- Count

template = """
!<INPUT 0>!

Given only the information above, what are !<INPUT 1>! most salient high-level questions we can answer about the subjects in the statements?
1)
"""


def run_gpt_prompt_focal_pt_v1(persona, statements, n, test_input=None, verbose=False):
  def create_prompt_input(persona, statements, n, test_input=None):
    prompt_input = [statements, str(n)]
    return prompt_input

  def get_fail_safe(n):
    return ["Who am I"] * n

  def __func_clean_up(gpt_response: FocalPoint, prompt=""):
    response_str = "1) " + ("\n".join(gpt_response.questions)).strip()
    ret = []
    for i in response_str.split("\n"):
      ret += [i.split(") ")[-1]]
    return ret

  def __func_validate(gpt_response, prompt=""):
    try:
      __func_clean_up(gpt_response, prompt)
      return True
    except:
      traceback.print_exc()
      return False

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
  prompt_template = "persona/prompt_template/v2/generate_focal_pt_v1.py"
  prompt_input = create_prompt_input(persona, statements, n)
  prompt = generate_prompt(prompt_input, prompt_template_str=template)

  fail_safe = get_fail_safe(n)
  output = safe_generate_structured_response(
    prompt, gpt_param, FocalPoint, 5, fail_safe, __func_validate, __func_clean_up
  )

  if debug or verbose:
    print_run_prompts(prompt_template, persona, gpt_param, prompt_input, prompt, output)

  return output, [output, prompt, gpt_param, prompt_input, fail_safe]
