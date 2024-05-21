import requests
import pandas as pd 
import base64
# import speech_recognition as sr
import os


# speak url

speak = "http://172.20.10.10/api/tts/speak?pitch=0&speechRate=0&flush=false"

record_url= 'http://172.20.10.10/api/audio/record/start'
stop_record_url = 'http://172.20.10.10/api/audio/record/stop'

get_audio_file = 'http://172.20.10.10/api/audio?fileName=test.wav&base64=false'

url = "http://172.20.10.10/api/tts/speak?pitch=0&speechRate=0&flush=false"


data = pd.read_csv('Participant_script.csv')
# recognizer = sr.Recognizer()

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

timeout=10

if __name__ == '__main__':
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

    name = input(f"Enter participant's name: ")
    placeholder = "NAME"

    # make a directory for the partecipant inside the audio out
    os.makedirs(f"Audio_out/Partecipant_{id}", exist_ok=True)
    
    # initialize partecipant dictionary
    partecipant_dict = {
        "Partecipant_id": id,
        "Task_1": [],
        "Task_2": [],
        "Task_3": []
    }
    number_principles = 3
    number_conversations = 3
    
    for i in range(number_principles):
        for j in range(number_conversations):

            for k in range(2):
                # robot speaks and record
                if k == 0:
                    print(f'Participant {id} - principle # {i+1} - conversation # {j+1}')
                    command = input("Press enter to start conversation")
                    robot_mess = partecipant_row.iloc[0, 4+i*6+j*2+k]
                    robot_mess = robot_mess.replace(placeholder, name)
                    print(f'\tRobot:\t{robot_mess}')

                    
                    # say the message out loud
                    body_mex = {
                        "text": robot_mess,
                        "pitch": 0,
                        "speechRate": 0,
                        "voice": None,
                        "flush": False,
                        "utteranceId": None,
                        "language": None
                    }
                    response = requests.post(url, json=body_mex)

                    human_msg = input("\tYou:\t")
                    partecipant_dict[f"Task_{i+1}"].append(human_msg)

                    # #start recording partecipant
                    # command = input("Press enter to start recording")
                    # filename=f"part_{id}_task_{i}_mex{k}"
                    # body_start_audio= { "fileName":filename }
                    # response = requests.post(record_url, json=body_start_audio)
                    # command = input("Press enter to stop recording")
                    
                    # #get audio file
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
                    command = input("Press enter to reveal response")
                    robot_mess = partecipant_row.iloc[0, 4+i*6+j*2+k]
                    print(f'\tRobot:\t{robot_mess}\n')
                    # # say the message out loud
                    body_mex = {
                        "text": robot_mess,
                        "pitch": 0,
                        "speechRate": 0,
                        "voice": None,
                        "flush": False,
                        "utteranceId": None,
                        "language": None
                    }
                    response = requests.post(url, json=body_mex)

    # convert partecipant dictionary to csv and save it
    partecipant_df = pd.DataFrame(partecipant_dict)
    partecipant_df.to_csv(f"Audio_out/Partecipant_{id}/partecipant_{id}_script.csv")

    
            
            