import requests
import pandas as pd 
import base64
import os

base_url = "http://192.168.43.230/"



def fetch_audio_with_timeout(url, timeout):
    try:
        response = requests.get(url, timeout=timeout)
        r_body = response.json()
        print(r_body.keys())
        results= r_body['result']
        print(results.keys())
        return results['contentType'], results['base64']
    except requests.RequestException as e:
        print(f"Error fetching the audio file: {e}")
        return None

def misty_speak(msg, utteranceId=None, flush=False, voice=None, language=None):
    url = base_url+"api/tts/speak"    
    body_mex = {
        "text": msg,
        "pitch": 0,
        "speechRate": 0,
        "voice": voice,
        "flush": flush,
        "utteranceId": utteranceId,
        "language": language
    }
    response = requests.post(url, json=body_mex)

def misty_display_image(FileName):
    url = base_url+"api/images/display"
    body_mex = {
        "FileName": FileName,
    }
    response = requests.post(url, json=body_mex)

def misty_play_audio(FileName):
    url = base_url+"api/audio/play"
    body_mex = {
        "FileName": FileName,
    }
    response = requests.post(url, json=body_mex)

# for available actions, consult /experimental study/actions.json
def misty_play_action(action_name):
    url = base_url+"api/actions/start"
    body_mex = {
        "name": action_name,
        "UseVisionData": False
    }
    response = requests.post(url, json=body_mex)

def save_base64_audio(encoded_str, content_type, output_file):
    # Decode the base64 string
    audio_data = base64.b64decode(encoded_str)

    # Determine the file extension based on the content type
    if content_type == 'audio/mpeg':
        file_extension = '.mp3'
    elif content_type == 'audio/wav':
        file_extension = '.wav'
    elif content_type == 'audio/ogg':
        file_extension = '.ogg'
    else:
        raise ValueError("Unsupported content type")

    # Append the correct file extension to the output file
    output_file += file_extension

    # Write the decoded data to a file
    with open(output_file, 'wb') as file:
        file.write(audio_data)

    print(f"Audio file saved as {output_file}")

def check_csv_structure(file_path, df_new):
    """
    Check if the CSV file has the same structure as the given DataFrame.
    """
    if not os.path.exists(file_path):
        # print("File does not exist. It will be created.")
        return False

    try:
        # Read the existing CSV file
        df_existing = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return False

    # Check if the column names match
    # existing_columns = list(df_existing.columns)
    # existing_columns.remove("Unnamed: 0")
    if list(df_existing.columns) != list(df_new.columns):
        print(f"Column names do not match. Expected: {list(df_new.columns)}, Found: {list(df_existing.columns)}")
        return False

    # print("The CSV file has the expected structure.")
    return True

timeout=10

expression = {
    "concerned" : "e_ApprehensionConcerned.jpg",
    "love" :"e_Love.jpg",
    "star_eyes":"e_EcstacyStarryEyed.jpg",
    "grief" : "e_Grief.jpg",
    "angry" : "e_Rage3.jpg",
    "admiration" : "s_Admiration.jpg",
    "fear" : "e_Fear.jpg",
    "default" : "e_DefaultContent.jpg"
}
sound = {
    "love" : "s_Love.wav",
    "ohhh" : "s_Acceptance.wav",
    "UhOh" : "s_PhraseUhOh.wav",
    "angry" : "s_Anger2.wav",
    "acceptance" : "s_Acceptance.wav",
    "disapproval" : "s_Disapproval.wav"
}

if __name__ == '__main__':
    
    # read predesigned response csv
    data = pd.read_csv('./experimental study/participant_script_third.csv')

    # get participant ID
    while True:
        try:
            id = int(input(f"Enter participant ID (0-{len(data.index)}): "))
            if 0 <= id <= len(data.index):
                break
            else:
                print(f"Please enter a number between 0 and {len(data.index)}.")
        except ValueError:
            print(f"Invalid input. Please enter an integer between 0 and {len(data.index)}.")
    # Get corresponding row from file
    partecipant_row = data[data['Partecipant_id'] == id]

    # get participant name
    name = input(f"Enter participant's name: ")
    placeholder = "NAME"

    # make a directory for the partecipant inside the audio out
    os.makedirs(f"Audio_out/Partecipant_{id}", exist_ok=True)
    
    number_principles = 3
    number_conversations = 3
    # initialize partecipant dictionary and dataframe
    partecipant_dict = {
        "Partecipant_id": id,
        "Partecipant_name": name,
        "Task_1": ["" for i in range(number_conversations)],
        "Task_2": ["" for i in range(number_conversations)],
        "Task_3": ["" for i in range(number_conversations)]
    }
    partecipant_df = pd.DataFrame(partecipant_dict)

    output_file_path = f"Audio_out/Partecipant_{id}/partecipant_{id}_script.csv"
    # Check the CSV file structure， if exists
    if check_csv_structure(output_file_path, partecipant_df):
        partecipant_df = pd.read_csv(output_file_path)
        partecipant_df.loc[:,"Partecipant_name"] = name
        print(f"Successfully read csv at {output_file_path}.")
        print(partecipant_df)
    

    # start testing, ask for principles tested
    while True:
        try:
            # 0     : run test on all principles
            # 1-3   : run test on specific principle
            principle_tested = int(input(f"Enter 0 to test all principles, or number (1-3) to test the specified principle: "))
            if 0 <= principle_tested <= number_principles:
                break
            else:
                print(f"Please enter a number between 0 and {number_principles}.")
        except ValueError:
            print(f"Invalid input. Please enter an integer between 0 and {number_principles}.")


    # testing all principles
    if(principle_tested == 0):
        for i in range(number_principles):
            for j in range(number_conversations):
                for k in range(2):
                    # conversation phase 1 - robot speaks
                    if k == 0:
                        print(f'Participant {id} - {name} - principle # {i+1} - conversation # {j+1}')
                        command = input("Press enter to start conversation")
                        if i == 0:
                            misty_play_action("think")
                        elif i == 1:
                            misty_play_action("walk-happy")
                        elif i == 2:
                            misty_play_action("body-reset")
                            misty_play_action("listen")
                        else:
                            misty_play_action("body-reset")
                        robot_mess = partecipant_row.iloc[0, 4+i*6+j*2+k]
                        robot_mess = robot_mess.replace(placeholder, name)
                        print(f'\tRobot:\t{robot_mess}')
                        misty_speak(robot_mess)

                        # conversation phase 2 - user answers
                        human_msg = input("\tYou:\t")
                        partecipant_df.loc[j, f"Task_{i+1}"] = human_msg

                    # conversation phase 3 - robot answers
                    if k == 1:
                        # success round
                        if j==2 and partecipant_row.iloc[0, 1+i]==1:
                            # success action + expression, basing on the tested principle 
                            if i == 0:
                                misty_play_action("love")
                            elif i == 1:
                                misty_play_action("angry")
                            elif i == 2:
                                misty_play_action("oops")

                        # normal round
                        else:
                            # normal action + expression, basing on the tested principle 
                            if i == 0:
                                misty_play_action("confused")
                            elif i == 1:
                                misty_play_action("concerned")
                            elif i == 2:
                                # misty_play_action("cheers")
                                misty_play_action("admire")
                        robot_mess = partecipant_row.iloc[0, 4+i*6+j*2+k]
                        print(f'\tRobot :\t{robot_mess}\n')
                        misty_speak(robot_mess)

    # testing specific principle
    else:
        i = principle_tested-1
        for j in range(number_conversations):
            for k in range(2):
                if k == 0:
                    print(f'Participant {id} - {name} - principle # {i+1} - conversation # {j+1}')
                    command = input("Press enter to start conversation")
                    if i == 0:
                        misty_play_action("think")
                    elif i == 1:
                        misty_play_action("walk-happy")
                    elif i == 2:
                        misty_play_action("body-reset")
                        misty_play_action("listen")
                    else:
                        misty_play_action("body-reset")
                    robot_mess = partecipant_row.iloc[0, 4+i*6+j*2+k]
                    robot_mess = robot_mess.replace(placeholder, name)
                    print(f'\tRobot:\t{robot_mess}')
                    misty_speak(robot_mess)

                    human_msg = input("\tYou:\t")
                    partecipant_df.loc[j, f"Task_{i+1}"] = human_msg
                
                if k == 1:
                    if j==2 and partecipant_row.iloc[0, 1+i]==1:
                        print("success")
                        if i == 0:
                            misty_play_action("love")
                        elif i == 1:
                            misty_play_action("angry")
                        elif i == 2:
                            misty_play_action("oops")

                    else:
                        if i == 0:
                            misty_play_action("confused")
                        elif i == 1:
                            misty_play_action("concerned")
                        elif i == 2:
                            misty_play_action("admire")
                    robot_mess = partecipant_row.iloc[0, 4+i*6+j*2+k]
                    print(f'\tRobot :\t{robot_mess}\n')
                    misty_speak(robot_mess)

    # convert partecipant dictionary to csv and save it
    partecipant_df.to_csv(output_file_path, index=False)

            
            