from pydantic import BaseModel
import traceback
from typing import Any

from utils import debug
from ..common import openai_config, get_prompt_file_path
from ..gpt_structure import safe_generate_structured_response
from ..print_prompt import print_run_prompts


def create_prompt(prompt_input: dict[str, Any]):
  conversation = prompt_input["conversation"]
  persona_1_name = prompt_input["persona_1_name"]
  persona_1_schedule_decomp = prompt_input["person_1_schedule_decomp"]
  curr_time = prompt_input["curr_time"]
  
  prompt = f"""
[Conversation]
{conversation}
[End of conversation]

[{persona_1_name}'s Current Daily Plan at the current time {curr_time}]
{persona_1_schedule_decomp}
[End of {persona_1_name}'s Current Daily Current Plan]

Write down if there is anything from the conversation that {persona_1_name} needs to remember for their planning, from {persona_1_name}'s perspective, in a full sentence. Take the current Daily Plan into account. Start the sentence with {persona_1_name}'s name.
"""
  return prompt


class PlanningThought(BaseModel):
  planning_thought: str


def run_gpt_prompt_planning_thought_on_convo(
  persona, all_utterances, test_input=None, verbose=False
):
  def create_prompt_input(persona, all_utterances, test_input=None):
    prompt_input = {
      "conversation": all_utterances,
      "persona_1_name": persona.scratch.name,
      "person_1_schedule_decomp": persona.scratch.f_daily_schedule,
      "curr_time":persona.scratch.curr_time.strftime("%B %d, %Y, %H:%M:%S %p")
    }
    return prompt_input

  def __func_clean_up(gpt_response: PlanningThought, prompt=""):
    return gpt_response.planning_thought.strip().strip('"').strip()

  def __func_validate(gpt_response, prompt=""):
    try:
      if not isinstance(gpt_response, PlanningThought):
        return False
      __func_clean_up(gpt_response, prompt)
      return True
    except Exception:
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
  prompt_file = get_prompt_file_path(__file__)
  prompt_input = create_prompt_input(persona, all_utterances)
  prompt = create_prompt(prompt_input)

  fail_safe = get_fail_safe()
  output = safe_generate_structured_response(
    prompt,
    gpt_param,
    PlanningThought,
    5,
    fail_safe,
    __func_validate,
    __func_clean_up,
  )

  if debug or verbose:
    print_run_prompts(prompt_file, persona, gpt_param, prompt_input, prompt, output)

  return output, [output, prompt, gpt_param, prompt_input, fail_safe]
