import requests
import pandas as pd 
import base64
import speech_recognition as sr
import os


# speak url

speak = "http://192.168.241.230/api/tts/speak?pitch=0&speechRate=0&flush=false"

record_url= 'http://192.168.241.230/api/audio/record/start'
stop_record_url = 'http://192.168.241.230/api/audio/record/stop'

get_audio_file = 'http://192.168.241.230/api/audio?fileName=test.wav&base64=false'

url = "http://192.168.241.230/api/tts/speak?pitch=0&speechRate=0&flush=false"


data = pd.read_csv('Participant_script.csv')
recognizer = sr.Recognizer()

def fetch_audio_with_timeout(url, timeout):
    try:
        response = requests.get(url, timeout=timeout)
        r_body = response.json()
        r_body.contentType, r_body.base64
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
    id = input("Enter participant ID: ")
    # get pertecipant row
    partecipant_row = data[data['Partecipant_id'] == int(id)]
    # make a directory for the partecipant inside the audio out
    os.makedirs(f"Audio_out/Partecipant_{id}", exist_ok=True)
    
    # initialize partecipant dictionary
    partecipant_dict = {
        "Partecipant_id": id,
        "Task_1": [],
        "Task_2": [],
        "Task_3": []
    }
    
    for i in range(3):
        for k in range(4,6):
            command = input("Press enter to preceed")
            robot_mess = partecipant_row.iloc[0, k]
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
            
            #start recording partecipant
            command = input("Press enter to start recording")
            filename=f"part_{id}_task_{i}_mex{k-4}"
            body_start_audio= { "fileName":filename }
            response = requests.post(record_url, json=body_start_audio)
            command = input("Press enter to start recording")
            
            #get audio file
            response = requests.post(stop_record_url, json={})
            file_response= f"http://192.168.241.230/api/audio?fileName={filename}.wav&base64=true"
            content_type, base64_file = fetch_audio_with_timeout(file_response, timeout)
            save_base64_audio(base64_file, content_type, f"Audio_out/Partecipant_{id}/{filename}")
            
            # convert autio to text
            with sr.AudioFile(f"Audio_out/Partecipant_{id}/{filename}.wav") as source:
                audio_text = recognizer.record(source)
                text = recognizer.recognize_google(audio_text)
                print(text)
                # appnd to the partecipant dictionary
                partecipant_dict[f"Task_{i+1}"].append(text)
    # convert partecipant dictionary to csv and save it
    partecipant_df = pd.DataFrame(partecipant_dict)
    partecipant_df.to_csv(f"Audio_out/Partecipant_{id}/partecipant_{id}_script.csv")

    
            
            