"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: print_prompt.py
Description: For printing prompts when the setting for verbose is set to True.
"""

##############################################################################
#                    PERSONA Chapter 1: Prompt Structures                    #
##############################################################################


def print_run_prompts(
    prompt_file="",
    persona=None,
    gpt_param=None,
    prompt_input=None,
    prompt="",
    output=None,
):
    print(f"=== File: {prompt_file}")
    print("~~~ persona    ---------------------------------------------------")
    print(persona.name if persona else "None", "\n")
    print("~~~ gpt_param ----------------------------------------------------")
    print(gpt_param, "\n")
    print("~~~ prompt_input    ----------------------------------------------")
    print(prompt_input, "\n")
    print("~~~ final prompt    ----------------------------------------------------")
    print(prompt, "\n")
    print("~~~ processed output    ----------------------------------------------------")
    print(output, "\n")
    print("=== END ==========================================================")
    print("\n\n\n")
