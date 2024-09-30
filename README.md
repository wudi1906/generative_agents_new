

# Generative Agents Collaboratively Mission Planning 

<p align="center" width="100%">
<img src="cover.png" alt="Smallville" style="width: 80%; min-width: 300px; display: block; margin: auto;">
</p>

This repository is an evolution of the repository based on the paper "[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)."

_______________________________________
## Index:
1. [Setup](#setting-up-the-environment)
2. [Execution](#running-a-simulation)
3. [Cost-Tracking](#cost-tracking)
_______________________________________

## Setting Up The Environment

### Step 1. Conda Env

Note: If you change the environment name from `simulacra`, you'll need to update the name in the upcoming bash scripts as well.
```bash
    conda create -n simulacra python=3.9.12 pip
    conda activate simulacra
    pip install -r requirements.txt
```


### Step 2. OpenAI Config

Create a file called `openai_config.json` in the root directory.\
Azure example:
```json
{
    "client": "azure", 
    "model": "gpt-35-turbo-0125",
    "model-key": "<API-KEY>",
    "model-endpoint": "<MODEL-ENDPOINT>",
    "model-api-version": "<API-VERSION>",
    "model-costs": {
        "input":  0.5,
        "output": 1.5
    },
    "embeddings-client": "azure",
    "embeddings": "text-embedding-3-small",
    "embeddings-key": "<API-KEY>",
    "embeddings-endpoint": "<EMBEDDING-MODEL-ENDPOINT>",
    "embeddings-api-version": "<API-VERSION>",
    "embeddings-costs": {
        "input": 0.02,
        "output": 0.0
    },
    "experiment-name": "simulacra-test",
    "cost-upperbound": 10
}
```
OpenAI example:
```json
{
    "client": "openai", 
    "model": "gpt-3.5-turbo-0125",
    "model-key": "<API-KEY>",
    "model-costs": {
        "input":  0.5,
        "output": 1.5
    },
    "embeddings-client": "openai",
    "embeddings": "text-embedding-3-small",
    "embeddings-key": "<API-KEY>",
    "embeddings-costs": {
        "input": 0.02,
        "output": 0.0
    },
    "experiment-name": "simulacra-test",
    "cost-upperbound": 10
}
```

Feel free to change and test also other models (and change accordingly the input and output costs).\
Be aware that the only supported clients are **azure** and **openai**.\
The generation and the embedding models are configured separately to be able to use different clients.\
Change also the `cost-upperbound` according to your needs (the cost computation is done using "[openai-cost-logger](https://github.com/drudilorenzo/openai-cost-logger)" and the costs are specified per million tokens).

Next, you will (for now) also need to set up the `utils.py` file as described in the [original repo's README](README_origin.md). After creating the file as described there, add these lines to it and change them as necessary:

```
use_openai = True
# If you're not using OpenAI, define api_model
api_model = ""
```

## Running a simulation

> All the following scripts automatically activate a conda environment called `simulacra` using a conda installation at the following path: `/home/${USER}/anaconda3/bin/activate`.\
> You may want to change this line in case you are using a different conda installation (like miniconda) or conda environment name.

### Step 1. Starting the Environment Server
If you're running the backend in headless mode (see below), you can skip this step.

```bash
    ./run_frontend.sh <PORT-NUMBER>
```
 >Note: omit the port number to use the default 8000.

### Step 2. Starting the Simulation Server

#### Option 1: Running the server manually
```bash
    ./run_backend.sh <ORIGIN> <TARGET>
```
Example:
```bash
    ./run_backend.sh base_the_ville_isabella_maria_klaus simulation-test
```

See the [original README](README_origin.md) for commands to pass to the server when running it manually. In addition to the commands listed there, you can also use the command `headless` in place of `run` (i.e. `headless 360` rather than `run 360`) to run in headless mode.

#### Option 2. Automatic Execution
The following script offer a range of enhanced features:
- `Automatic Saving`: The simulation automatically saves progress every 200 steps, ensuring you never lose data.
- `Error Recovery`: In the event of an error, the simulation automatically resumes by stepping back and restarting from the last successful point. This is crucial as the model relies on formatted answers, which can sometimes cause exceptions.
- `Automatic Tab Opening`: A new browser tab will automatically open when necessary.
- `Headless Mode`: The scripts support running simulations in headless mode, enabling execution on a server without a UI. There are two different headless modes: Passing "None" runs in pure headless mode (no browser needed), whereas passing "False" runs in Chrome's builtin headless mode (needs [headless-chrome](https://developer.chrome.com/blog/headless-chrome) installed). Prefer "None" over "False" in normal cases.
- `Configurable Port Number`: You can configure the port number as needed.

For more details, refer to: [run_backend_automatic.sh](https://github.com/drudilorenzo/generative_agents/blob/fix-and-improve/run_backend_automatic.sh) and [automatic_execution.py](https://github.com/drudilorenzo/generative_agents/blob/fix-and-improve/reverie/backend_server/automatic_execution.py).
```bash
    ./run_backend_automatic.sh -o <ORIGIN> -t <TARGET> -s <STEP> --ui <True|None|False> -p <PORT> --browser_path <BROWSER-PATH>
```
Note: The step argument means the simulation will **end after** step number `<STEP>`, not necessarily **run for** that number of steps.

Example:
```bash
    ./run_backend_automatic.sh -o base_the_ville_isabella_maria_klaus -t test_1 -s 4 --ui None
```

### Endpoint list
- [http://localhost:8000/](http://localhost:8000/) - check if the server is running
- [http://localhost:8000/simulator_home](http://localhost:8000/simulator_home) - watch the live simulation
- `http://localhost:8000/replay/<simulation-name>/<starting-time-step>` - replay a simulation

For a more detailed explanation see the [original readme](README_origin.md).


## Cost Tracking

For the cost tracking is used the package "[openai-cost-logger](https://github.com/drudilorenzo/openai-cost-logger)". Given the possible high cost of a simulation,  you can set a cost upperbound in the config file to be able to raise an exception and stop the execution when it is reached.

See all the details of your expenses using the notebook "[cost_viz.ipynb](https://github.com/drudilorenzo/generative_agents/blob/main/cost_viz.ipynb)."

## Cost Assessment

### 1. base_the_ville_isabella_maria_klaus

- **Model**: "gpt-3.5-turbo-0125"
- **Embeddings**: "text-embedding-3-small"
- **N. Agents**: 3
- **Steps**: ~5000
- **Final Cost**: ~0.31 USD

### 2. base_the_ville_n25

- See the simulation saved: [skip-morning-s-14](https://github.com/drudilorenzo/generative_agents/tree/fix-and-improve/environment/frontend_server/storage/skip-morning-s-14)
- **Model**: "gpt-3.5-turbo-0125"
- **Embeddings**: "text-embedding-3-small"
- **N. Agents**: 25
- **Steps**: ~3000 (until ~8 a.m.)
- **Final Cost**: ~1.3 USD

### 3. base_the_ville_n25

- **Model**: "gpt-3.5-turbo-0125"
- **Embeddings**: "text-embedding-3-small"
- **N. Agents**: 25
- **Steps**: ~8650 (full day)
- **Final Cost**: ~18.5 USD
