def ChatGPT_safe_generate_response(
  prompt,
  example_output,
  special_instruction,
  repeat=3,
  fail_safe_response="error",
  func_validate=None,
  func_clean_up=None,
  verbose=False,
):
  
  if func_validate and func_clean_up:
    # prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
    prompt = '"""\n' + prompt + '\n"""\n'
    prompt += (
      f"Output the response to the prompt above in json. {special_instruction}\n"
    )
    prompt += "Example output json:\n"
    prompt += '{"output": "' + str(example_output) + '"}'

    if verbose:
      print("LLM PROMPT")
      print(prompt)

    for i in range(repeat):
      try:
        chatgpt_response = ChatGPT_request(prompt)
        if not chatgpt_response:
          raise Exception("No valid response from LLM.")
        curr_gpt_response = chatgpt_response.strip()
        end_index = curr_gpt_response.rfind("}") + 1
        curr_gpt_response = curr_gpt_response[:end_index]
        curr_gpt_response = json.loads(curr_gpt_response)["output"]

        if verbose:
          print("---- repeat count:", i)
          print("~~~~ curr_gpt_response:")
          print(curr_gpt_response)
          print("~~~~")

        if func_validate(curr_gpt_response, prompt=prompt):
          return func_clean_up(curr_gpt_response, prompt=prompt)

      except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()

  return fail_safe_response