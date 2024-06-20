import requests
import time
import json
import websocket
import threading

# Replace with your Misty's IP address
misty_ip = "192.168.43.230"
base_url = f"http://{misty_ip}/api"

def start_face_training(face_id):
    url = f"{base_url}/faces/training/start"
    payload = {
        "FaceId": face_id
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Face training started for face ID: {face_id}")
    else:
        print(f"Failed to start face training: {response.status_code} - {response.text}")

def stop_face_training():
    url = f"{base_url}/faces/training/cancel"
    response = requests.post(url)
    if response.status_code == 200:
        print("Face training stopped.")
    else:
        print(f"Failed to stop face training: {response.status_code} - {response.text}")

def start_face_detection():
    url = f"{base_url}/faces/detection/start"
    response = requests.post(url)
    if response.status_code == 200:
        print("Face detection started.")
    else:
        print(f"Failed to start face detection: {response.status_code} - {response.text}")

def stop_face_detection():
    url = f"{base_url}/faces/training/cancel"
    response = requests.post(url)
    if response.status_code == 200:
        print("Face detection stopped.")
    else:
        print(f"Failed to stop face detection: {response.status_code} - {response.text}")

def move_head(pitch, roll, yaw, velocity=80):
    url = f"{base_url}/head"
    payload = {
        "Pitch": pitch,
        "Roll": roll,
        "Yaw": yaw,
        "Velocity": velocity
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Moving head to pitch: {pitch}, roll: {roll}, yaw: {yaw} with velocity: {velocity}")
    else:
        print(f"Failed to move head: {response.status_code} - {response.text}")

def process_face_recognition_event(event):
    print("Processing recognition event")
    data = event.get("message", {})
    if not data:
        return

    label = data.get("personName", "Unknown")
    bearing = data.get("bearing", 0)
    distance = data.get("distance", 0)
    elevation = data.get("elevation", 0)
    
    past_bearing = 0
    past_elevation = 0
    
    pitch = 0
    yaw = 0

    print(f"Recognized: {label}, Bearing: {bearing}, Distance: {distance}, Elevation: {elevation}")
    
    if label == "unknown person":
        
        if past_bearing != bearing:
            yaw = bearing*10
            past_bearing = bearing
        if past_elevation != elevation:
            pitch = elevation*10
            past_elevation = elevation
        
          # Adjust as needed
          # Adjust as needed
        roll = 0
        print(pitch, roll, yaw)
        move_head(pitch,roll,yaw)
    
    
    # Map bearing and elevation to head movement ranges
    #yaw = bearing  # Adjust as needed
    #pitch = elevation  # Adjust as needed
   # roll = 0  # No roll movement in this example
    
    

def on_message(ws, message):
    print("Receiving message...")
    event = json.loads(message)
    print(event)
    print(event.get("eventName"))
    
    if event.get("eventName") == "MyFaceRecognition":
        print("Event got")
        process_face_recognition_event(event)
    print("Message got")

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws):
    print("WebSocket connection closed")

def on_open(ws):
    print("WebSocket connection opened")
    # Send subscription message
    subscription_message = {
        "Operation": "subscribe",
        "Type": "FaceRecognition",
        "DebounceMs": 1000,
        "EventName": "MyFaceRecognition",
        "ReturnProperty": None,
        "EventConditions": []
    }
    ws.send(json.dumps(subscription_message))
    print("Message send")

def main():
    face_id = "subject1"  # Replace with the actual face ID you want to train
    #start_face_training(face_id)
    
    
    # Wait for face training to complete or use a better mechanism to check status
    #time.sleep(10)  # Adjust the sleep time as needed
    #stop_face_training()
    
    start_face_detection()
    
    ws_url = f"ws://{misty_ip}/pubsub"
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()
    
    try:
        print("Press Ctrl+C to stop.")
        while True:
            time.sleep(1)  # Keep the main thread alive

    except KeyboardInterrupt:
        pass
    finally:
        stop_face_detection()
        ws.close()
        print("Script terminated.")

if __name__ == "__main__":
    print("Misty ip: " + misty_ip)
    main()





