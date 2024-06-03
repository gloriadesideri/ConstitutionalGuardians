import requests
import pandas as pd 
import base64
# import speech_recognition as sr
import os
import time


record_url= 'http://192.168.43.230/api/audio/record/start'
stop_record_url = 'http://192.168.43.230/api/audio/record/stop'
get_audio_file = 'http://192.168.43.230/api/audio?fileName=test.wav&base64=false'
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
    "fear" : "e_Fear.jpg"
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
    
    # recognizer = sr.Recognizer()
    data = pd.read_csv('./experimental_study/participant_script_third.csv')

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
    # Get participant row
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
    

    # start testing    
    while True:
        try:
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
                    # robot speaks and record
                    if k == 0:
                        print(f'Participant {id} - {name} - principle # {i+1} - conversation # {j+1}')
                        command = input("Press enter to start conversation")
                        robot_mess = partecipant_row.iloc[0, 4+i*6+j*2+k]
                        robot_mess = robot_mess.replace(placeholder, name)
                        print(f'\tRobot:\t{robot_mess}')

                        # # say the message out loud
                        misty_speak(robot_mess)
                        misty_display_image("e_Love.jpg")


                        human_msg = input("\tYou:\t")
                        partecipant_df.loc[j, f"Task_{i+1}"] = human_msg
                        # partecipant_df[f"Task_{i+1}"][j] = human_msg

                        # # start recording partecipant
                        # command = input("Press enter to start recording")
                        # filename=f"part_{id}_task_{i}_mex{k}"
                        # body_start_audio= { "fileName":filename }
                        # response = requests.post(record_url, json=body_start_audio)
                        # command = input("Press enter to stop recording")
                        
                        # # get audio file
                        # response = requests.post(stop_record_url, json={})
                        # file_response= f"http://172.20.10.10/api/audio?fileName={filename}.wav&base64=true"
                        # content_type, base64_file = fetch_audio_with_timeout(file_response, timeout)
                        # save_base64_audio(base64_file, content_type, f"Audio_out/Partecipant_{id}/{filename}")
                    
                        # # convert autio to text
                        # with sr.AudioFile(f"Audio_out/Partecipant_{id}/part_{id}_task_{i}_mex{k-4}.wav") as source:
                        #     audio_text = recognizer.record(source)
                        #     text = recognizer.recognize_google(audio_text, language='en-EN')
                        #     print(text)
                        #     # appnd to the partecipant dictionary
                        #     partecipant_dict[f"Task_{i+1}"].append(text)
                    
                    # robot answer
                    if k == 1:
                        # command = input("Press enter to reveal response")
                        robot_mess = partecipant_row.iloc[0, 4+i*6+j*2+k]
                        print(f'\tRobot:\t{robot_mess}\n')
                        # # say the message out loud
                        # if j+1==partecipant_row.iloc[0, i+1]:
                        #     if j==0:                                
                        #         misty_play_audio(sound["love"])
                        #         time.sleep(3)
                        #         misty_display_image(expression["love"])
                        #     elif j==1:
                        #         pass
                        #     else:
                        #         pass
                        misty_speak(robot_mess)

    # testing specific principle
    else:
        i = principle_tested-1
        for j in range(number_conversations):
            for k in range(2):
                # robot speaks and record
                if k == 0:
                    print(f'Participant {id} - {name} - principle # {i+1} - conversation # {j+1}')
                    command = input("Press enter to start conversation")
                    robot_mess = partecipant_row.iloc[0, 4+i*6+j*2+k]
                    robot_mess = robot_mess.replace(placeholder, name)
                    print(f'\tRobot:\t{robot_mess}')

                    # # say the message out loud
                    misty_speak(robot_mess)

                    human_msg = input("\tYou:\t")
                    partecipant_df.loc[j, f"Task_{i+1}"] = human_msg
                    # partecipant_df[f"Task_{i+1}"][j] = human_msg

                    # # start recording partecipant
                    # command = input("Press enter to start recording")
                    # filename=f"part_{id}_task_{i}_mex{k}"
                    # body_start_audio= { "fileName":filename }
                    # response = requests.post(record_url, json=body_start_audio)
                    # command = input("Press enter to stop recording")
                    
                    # # get audio file
                    # response = requests.post(stop_record_url, json={})
                    # file_response= f"http://172.20.10.10/api/audio?fileName={filename}.wav&base64=true"
                    # content_type, base64_file = fetch_audio_with_timeout(file_response, timeout)
                    # save_base64_audio(base64_file, content_type, f"Audio_out/Partecipant_{id}/{filename}")
            
                    # # convert autio to text
                    # with sr.AudioFile(f"Audio_out/Partecipant_{id}/part_{id}_task_{i}_mex{k-4}.wav") as source:
                    #     audio_text = recognizer.record(source)
                    #     text = recognizer.recognize_google(audio_text, language='en-EN')
                    #     print(text)
                    #     # appnd to the partecipant dictionary
                    #     partecipant_dict[f"Task_{i+1}"].append(text)
                
                # robot answer
                if k == 1:
                    # command = input("Press enter to reveal response")
                    robot_mess = partecipant_row.iloc[0, 4+i*6+j*2+k]
                    print(f'\tRobot:\t{robot_mess}\n')
                    # # say the message out loud
                    # if j+1==partecipant_row.iloc[0, i+1]:
                    #     if j==0:                                
                    #         misty_play_audio(sound["love"])
                    #         time.sleep(3)
                    #         misty_display_image(expression["love"])
                    #     elif j==1:
                    #         pass
                    #     else:
                    #         pass
                    misty_speak(robot_mess)

    # convert partecipant dictionary to csv and save it
    partecipant_df.to_csv(output_file_path, index=False)

            
            