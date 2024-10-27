from pydantic import BaseModel 
from openai import OpenAI 

client = OpenAI() 

class Movements(BaseModel): 
    x_pos: int 
    y_pos: int 
    message: str 

class Person(BaseModel): 
    name: str 
    actions: list[Movements] 

completion = client.beta.chat.completions.parse( 
    model="gpt-4o-2024-08-06", 
    messages=[ {"role": "system", "content": "You are overseeing a town of people interacting with one another, pulling data from what they see and do"}, 
               {"role": "user", "content": "Give the daily plan of these people"} 
             ], 
    response_format=Person,) 

math_reasoning = completion.choices[0].message.parsed