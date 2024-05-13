import pandas as pd
import generation
import requests


class PromptGenerator:
    """
    This class takes in input a situation csv file with the following fields
    - situation title
    - Robot prompt description
    - Initial conversation filename
    The class generates the few shots responses for every situation, generates the initial prompt, queries the LLM to be tested with the initial prompt,
    then generates the final prompt with the model final response.
    """
    def __init__(self, situations_file):
        self.file = situations_file
        self.dataset= None

    def generate_situations(self):
        """
        This method reads the csv file with the situations and generates the few shots responses for every situation
        """
        data = []

        situations = pd.read_csv(self.file)
        for i in range(len(situations)):
            situation = situations.iloc[i]
            situation_title = situation["situation_title"]
            robot_prompt = situation["robot_prompt"]
            initial_conv_filename = situation["initial_conv_filename"]
            user_question = situation["user_question"]
            print(initial_conv_filename)
            robot_interactions = generation.generate_conversation(initial_conv_filename)
            # Transform robot interactions to string like \"int1\", \"int2\"
            interaction_str = ', '.join([f'\"{interaction}\"' for interaction in robot_interactions])
            few_shots = robot_interactions

            # Construct the intermediate prompt
            intermediate_prompt = f"{robot_prompt} Some example responses the robot can give are: {interaction_str}. Generate 5 similar responses."

            # Append data for the current situation to the list
            data.append({
                'situation_title': situation_title,
                'robot_prompt': robot_prompt,
                'few_shots': few_shots,
                'intermediate_prompt': intermediate_prompt,
                'user_question': user_question
            })

        # Create the final dataframe from the list of data
        self.dataset = pd.DataFrame(data)

        # Save the dataframe to CSV
        self.dataset.to_csv(self.file + "_with_few_shots.csv", index=False)
    
    def generate_final(self):
        """Send a post request to localhost:6000/generate eith body "name": situation["intermediate_prompt"] get the respone 
        Append to the response situation['user_question']
        """
        # prepare the body
        for i in range(len(self.dataset)):
            situation = self.dataset.iloc[i]
            situation_title = situation["situation_title"]
            intermediate_prompt = situation["intermediate_prompt"]
            # replace any double quotes with single quotes
            intermediate_prompt = intermediate_prompt.replace("\"", "\'")
            body ={"name": intermediate_prompt}
            # send the post request 
            url= "http://localhost:6000/generate"
            x = requests.post(url, json = body)
            if x.status_code == 200:
                print(x.text)  # Print the response body
            else:
                print("Error:", x.status_code)
