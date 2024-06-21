import os
import pandas as pd

# Path to the main directory containing participant folders
main_dir = 'Audio_out'

# Loop through each participant folder
for participant_folder in os.listdir(main_dir):
    folder_path = os.path.join(main_dir, participant_folder)
    if os.path.isdir(folder_path):
        # Extract participant ID from the folder name
        participant_id = participant_folder.split('_')[1]
        
        # Construct the path to the participant's CSV file
        csv_filename = f'partecipant_{participant_id}_script.csv'
        csv_path = os.path.join(folder_path, csv_filename)
        
        # Read the CSV file
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            
            # Process each task
            for task_num in range(1, 4):
                # Create a new DataFrame for the task
                task_df = pd.DataFrame({
                    'Agent': ['Human'] * len(df),
                    'Message': df[f'Task_{task_num}']
                })
                
                # Save the new DataFrame to a CSV file
                output_filename = f'{participant_folder}_task_{task_num}.csv'
                output_path = os.path.join(folder_path, output_filename)
                task_df.to_csv(output_path, index=False)

print("Script executed successfully!")
