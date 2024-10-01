from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import requests
import base64
import json

app = FastAPI()

# Define the input model for the text request
class TextInput(BaseModel):
    text: str
    output_format: str = "base64"  # Default output is base64, but can be binary


# Split the text into chunks based on max length
def split_text_into_chunks(text, max_length=280):
    chunks = []
    while text:
        chunk = text[:max_length]
        text = text[max_length:]
        chunks.append(chunk)
    return chunks

# Generate audio for each chunk
def generate_audio(chunk):
    url = "https://api.tiktokv.com/media/api/text/speech/invoke/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "User-Agent": "com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)",
        "Cookie": "sessionid=581a1225c93f9b4bb9aacc49e4ebc5a9"
    }
    data = {
        "req_text": chunk,
        "speaker_map_type": 0,
        "aid": 1233,
        "text_speaker": "id_female_icha"
    }
    response = requests.post(url, headers=headers, data=data)
    response_json = response.json()
    if response_json["status_code"] == 0:
        return response_json["data"]["v_str"]
    else:
        raise HTTPException(status_code=500, detail="Failed to generate audio")

# Concatenate base64 MP3 chunks
def concatenate_base64_mp3(encoded_files):
    final_audio_data = b""
    for i, encoded_data in enumerate(encoded_files):
        decoded_data = base64.b64decode(encoded_data)
        if i == 0:
            final_audio_data += decoded_data
        else:
            # If it's not the first chunk, we may need to remove ID3 tags
            header = decoded_data[:10]
            if header[:3] == b'ID3':  # Check if there is an ID3 tag
                tag_size = int.from_bytes(header[6:10], byteorder='big')
                decoded_data = decoded_data[10 + tag_size:]
            final_audio_data += decoded_data
    return final_audio_data

# Main endpoint to receive text and return TTS in base64 or binary
@app.post("/tts")
async def tts_endpoint(input: TextInput, response: Response):
    text = input.text
    output_format = input.output_format.lower()
    
    # Split the input text into chunks if it's too long
    chunks = split_text_into_chunks(text)
    
    base64_strings = []
    for chunk in chunks:
        base64_string = generate_audio(chunk)
        base64_strings.append(base64_string)
    
    # Concatenate the base64 audio strings
    concatenated_audio = concatenate_base64_mp3(base64_strings)

    if output_format == "binary":
        # Return binary audio file
        response.headers["Content-Type"] = "audio/mpeg"
        return Response(content=concatenated_audio, media_type="audio/mpeg")
    elif output_format == "base64":
        # Convert binary audio to base64 and return as JSON
        final_base64_audio = base64.b64encode(concatenated_audio).decode("utf-8")
        return {"audio_base64": final_base64_audio}
    else:
        # Invalid format
        raise HTTPException(status_code=400, detail="Invalid output format. Choose 'base64' or 'binary'.")
