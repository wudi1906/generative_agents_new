'''
A script downlowds models from hugging face to local paths.
'''

import transformers 
from huggingface_hub import snapshot_download 

model = 'deepseek-ai/DeepSeek-R1-Distill-Llama-7B'
model_path = '/cephfs/wenchanggao/large-models/DeepSeek-R1-Distill-Llama-7B' 
snapshot_download(repo_id=model, local_dir=model_path, local_dir_use_symlinks=False)