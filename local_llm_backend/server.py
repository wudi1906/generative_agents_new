'''
Starts a server that loads local LLMs, generates embeddings, and responds 
requests in the format defined in bindings.py.
'''

import socket 
import requests 
import argparse
import torch
import os

from transformers import AutoTokenizer, AutoModelForCausalLM 

device = 'cpu'

model_to_path = {
  'DeepSeek-R1-Distill-Llama-7B': '/cephfs/wenchanggao/large-models/DeepSeek-R1-Distill-Llama-7B'
}

def receive_full_message(c_socket: socket.socket, buff_size: int=1028) -> bytes: 
  '''
  Receives long messages from the socket with chunks and concatenates them.

  Params: 
    <c_socket>: socket.socket, the client socket sending message 
    <buff_size>: int, the buffer size for chunks 
  
  Returns:
    <message>, bytes, the bytes of received message
  '''
  message = b''
  while True: 
    chunk = c_socket.recv(buff_size)
    if not chunk: 
      break
    message += chunk 
  return message

def start_server(port: int) -> socket.socket:
  s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s_socket.bind(('localhost', port))
  s_socket.listen(5)
  print(f'Listening on port {port}') 
  return s_socket

def load_local_model(model_name: str, device_id: int) -> tuple[AutoTokenizer, AutoModelForCausalLM]:
  '''
  Loads local model into GPU <device_id>. 

  Params: 
    <model_name>: str, the name of LLM to be loaded 
    <device_id>: int, the id of GPU for current server

  ReturnsL
    (<tokenizer>, <model>): the loaded tokenizer and model
  '''
  path = model_to_path[model_name]
  tokenizer = AutoTokenizer.from_pretrained(path, device_map=f'cuda:{device_id}') 
  model = AutoModelForCausalLM.from_pretrained(path, device_map=f'cuda:{device_id}')
  return (tokenizer, model)

def get_response(tokenizer: AutoTokenizer, model: AutoModelForCausalLM, prompt: str, max_length=1000, temperature=0.7): 
  '''
  Generates response with local LLM. TODO: finish bindings
  '''
  tokens = tokenizer(prompt, return_tensors='pt').to(device)
  with torch.no_grad():
    output_tokens = model.generate(**tokens, max_length=max_length, temperature=temperature, do_sample=True)
  return tokenizer.decode(output_tokens[0], skip_special_tokens=True)


def server(port: int, model_name: str, max_length: int, temperature: float) -> None: 
  '''
  A TCP server listens to port <port>, loads local models, parses received messages from agents, 
  wraps responses and sends instances back to the agents.

  Params: 
    <port>: int, the port current server listens to 
    <model_name>: str, the name of LLM to be loaded
  
  Returns: 
    None
  '''
  assert model_name in model_to_path, 'Unknown model name'
  tokenizer, model = load_local_model(model_name)
  s_socket = start_server(port) 
  while True: 
    c_socket, c_addr = s_socket.accept() 
    message = receive_full_message(c_socket=c_socket)
    message = str(message) 
    print(f'Received connection from {c_addr}') 
    response = get_response(tokenizer, model, message, max_length, temperature)
    c_socket.sendall(message.encode())
    print(f'Sent response {message}')


def main():
  global device
  parser = argparse.ArgumentParser() 
  parser.add_argument('--model', type=str, default='deepseek-ai/DeepSeek-R1-Distill-Llama-8B', help='Local language model') 
  parser.add_argument('--port', type=int, default=24642, help='Port number')
  parser.add_argument('--device_id', type=int, default=0, help='The id of GPU to use for this model. Set -1 to use cpu.')
  parser.add_argument('--max_length', type=int, default=1000, help='Maximum length of generated response')
  parser.add_argument('--temperature', type=float, default=0.7, help='Temperature for local model')
  args = parser.parse_args() 
  if args.device_id != -1:
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.device_id) # Specify one GPU for one server process temporarily. TODO: Is this good? 
    device = torch.device(f'cuda:{args.device_id}') 
  else: 
    os.environ['CUDA_VISIBLE_DEVICES'] = "" 
    device = torch.device('cpu')
  server(port=args.port, model_name=args.model)


if __name__ == '__main__':  
  start_server()
