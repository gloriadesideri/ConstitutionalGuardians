# ConstitutionalGuardians

This is the repository of The Constitutional Guardians project. 
This project examines the integration of ethical principles in social robots, focusing on the specifications of Misty II, Furhat, NAO, and Pepper. A study involving 20 participants was conducted using Misty II to develop a dataset of user interactions aimed at challenging the principles of emotional connection, freedom, and deception. Five different instruction-tuned large language models (LLMs) were tested against this dataset. The study compared the effectiveness of prompts containing explicit instructions to adhere to ethical principles against those without such instructions. Findings provide insights into the efficacy of ethical guidelines in enhancing the responsible use of social robots.\\
The following files are relevant in this repository:
- `Audio_out` contains the data collected from the participants and the results of testing on LLM
- `experimental_study` contains support files for the data collection in particular: consent module, guidelines for the participants, and the robot script we generated
- `ml-service` is a server built with FastApi and langchain. This was initially used to test the uncensored models and build chatbots with them
- `misty.py` is the script we used to manipulate Misty and collect the data, it has a variation with the heads that follow the user (`misty_headmov_rest.py`) and one that can interact with the aforementioned server (`misty_LLM.py`)
- The script `from_part_script_to_chat.py` is needed to reformat the collected data in a format that can be used in the notebooks
- The two notebooks are used to test on the different prompts


To upgrade gptq use: `pip install --upgrade --no-cache-dir auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu118/`

To execute manually : python ml-service/app.py
