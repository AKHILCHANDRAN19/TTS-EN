import asyncio
import re
import os
from edge_tts import Communicate

# Updated list of available voices
voices = {
    '1': 'en-AU-NatashaNeural',
    '2': 'en-AU-WilliamNeural',
    '3': 'en-CA-ClaraNeural',
    '4': 'en-CA-LiamNeural',
    '5': 'en-GB-LibbyNeural',
    '6': 'en-GB-MaisieNeural',
    '7': 'en-GB-RyanNeural',
    '8': 'en-GB-SoniaNeural',
    '9': 'en-GB-ThomasNeural',
    '10': 'en-HK-SamNeural',
    '11': 'en-HK-YanNeural',
    '12': 'en-IE-ConnorNeural',
    '13': 'en-IE-EmilyNeural',
    '14': 'en-IN-NeerjaExpressiveNeural',
    '15': 'en-IN-NeerjaNeural',
    '16': 'en-IN-PrabhatNeural',
    '17': 'en-KE-AsiliaNeural',
    '18': 'en-KE-ChilembaNeural',
    '19': 'en-NG-AbeoNeural',
    '20': 'en-NG-EzinneNeural',
    '21': 'en-NZ-MitchellNeural',
    '22': 'en-NZ-MollyNeural',
    '23': 'en-PH-JamesNeural',
    '24': 'en-PH-RosaNeural',
    '25': 'en-SG-LunaNeural',
    '26': 'en-SG-WayneNeural',
    '27': 'en-TZ-ElimuNeural',
    '28': 'en-TZ-ImaniNeural',
    '29': 'en-US-AnaNeural',
    '30': 'en-US-AndrewMultilingualNeural',
    '31': 'en-US-AndrewNeural',
    '32': 'en-US-AriaNeural',
    '33': 'en-US-AvaMultilingualNeural',
    '34': 'en-US-AvaNeural',
    '35': 'en-US-BrianMultilingualNeural',
    '36': 'en-US-BrianNeural',
    '37': 'en-US-ChristopherNeural',
    '38': 'en-US-EmmaMultilingualNeural',
    '39': 'en-US-EmmaNeural',
    '40': 'en-US-EricNeural',
    '41': 'en-US-GuyNeural',
    '42': 'en-US-JennyNeural',
    '43': 'en-US-MichelleNeural',
    '44': 'en-US-RogerNeural',
    '45': 'en-US-SteffanNeural',
    '46': 'en-ZA-LeahNeural',
    '47': 'en-ZA-LukeNeural'
}

# Function to preprocess text (removes unnecessary symbols and spaces)
def preprocess_text(text):
    # Replace multiple spaces or symbols with a single space
    text = re.sub(r'[^\w\s.,!?]', '', text)  # Remove special characters except punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Remove multiple spaces and trim
    return text

# Function to convert pitch selection to Hz
def convert_pitch_to_hz(pitch_choice):
    if pitch_choice == '1':  # -50%
        return '-50Hz'
    elif pitch_choice == '2':  # -25%
        return '-25Hz'
    elif pitch_choice == '3':  # Normal (0%)
        return '+0Hz'  # Ensure correct format
    elif pitch_choice == '4':  # +25%
        return '+25Hz'
    elif pitch_choice == '5':  # +50%
        return '+50Hz'
    return '+0Hz'  # Default to normal

# Function to convert the manually entered speaking rate to percentage
def convert_rate_to_percentage(rate_choice):
    try:
        rate = int(rate_choice)
        if -100 <= rate <= 100:  # Ensure the value is between -100 and 100
            return f"{'+' if rate >= 0 else ''}{rate}%"
    except ValueError:
        return '+0%'  # Default to normal if the input is invalid
    return '+0%'  # Default to normal

# Function to save text to speech
async def save_tts(text, selected_voice_code, rate, pitch):
    output_directory = "/storage/emulated/0/Download"  # Ensure this directory exists
    os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
    output_path = f"{output_directory}/{selected_voice_code}.mp3"  # Change path as needed

    communicate = Communicate(
        text,
        voice=selected_voice_code,
        rate=rate,
        pitch=pitch
    )
    try:
        await communicate.save(output_path)
        print(f"Audio saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

# Function to handle long text input
def get_long_text():
    print("\nEnter the text you want to convert to speech (type 'done' on a new line to finish):")
    input_text = []
    while True:
        line = input()
        if line.lower().strip() == 'done':
            break
        input_text.append(line)
    return preprocess_text(' '.join(input_text))

# Main function
async def main():
    print("Available Voices:")
    for key, value in voices.items():
        print(f"{key}: {value}")

    selected_voice_code = voices.get(input("Enter the number of the voice you want to use: "))

    if selected_voice_code:
        print("\nEnter speaking rate (-100 to 100):")
        rate_choice = input("Enter rate (e.g., -100, 0, 50, etc.): ")
        rate = convert_rate_to_percentage(rate_choice)

        print("\nChoose pitch:")
        print("1: -50%")
        print("2: -25%")
        print("3: Normal (0%)")
        print("4: +25%")
        print("5: +50%")
        pitch_choice = input("Select pitch option (1-5): ")
        pitch = convert_pitch_to_hz(pitch_choice)

        text = get_long_text()  # Get the long text or paragraph

        await save_tts(text, selected_voice_code, rate, pitch)

# Running the script
if __name__ == "__main__":
    asyncio.run(main())
