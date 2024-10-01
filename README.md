# FastAPI Text-to-Speech (TTS) API

This project is a simple **Text-to-Speech (TTS) API** built using **FastAPI**. It allows users to input text and receive audio in two formats: **base64-encoded audio** or **binary audio (MP3)**.

## Features

- Split long text into chunks (280 characters per chunk) to accommodate API limitations.
- Convert text to speech using a **private API** from **TikTok**.
- Return audio in either **base64** format (encoded as a string) or as **binary** (MP3 file).
- Implements FastAPI's auto-generated **Swagger UI** for easy API testing and documentation.

## Important Notice: Use of Private TikTok API

This project uses a **private Text-to-Speech API from TikTok**, which was obtained through **reverse engineering**. TikTok does not provide official public documentation for this API, and use of it may violate TikTok's terms of service.

The API is not intended for production use, and there are no guarantees of stability or continued access. TikTok may change or block access to this API at any time without warning. Use this API at your own risk.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn (ASGI server)
- Requests

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/agusibrahim/tiktok-tts-api
    cd tts-fastapi
    ```

2. Create and activate a virtual environment (optional, but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    If you don't have a `requirements.txt`, you can manually install dependencies:

    ```bash
    pip install fastapi uvicorn requests
    ```

## Running the API

1. Start the API server:

    ```bash
    uvicorn tts_api:app --reload
    ```

2. The API will be available at `http://127.0.0.1:8000`.

3. Access the **Swagger UI** at:

    ```url
    http://127.0.0.1:8000/docs
    ```

4. Alternatively, access the **ReDoc** documentation at:

    ```url
    http://127.0.0.1:8000/redoc
    ```

## API Endpoints

### `POST /tts`

- **Description**: Converts text to speech using the private TikTok API.
- **Request**:
    - `text`: The input text that needs to be converted into speech.
    - `output_format`: (Optional) Format of the response, can be either "base64" or "binary". Defaults to "base64".

- **Response**:
    - If `output_format` is `"base64"`, the response will be a JSON object with the base64-encoded audio string.
    - If `output_format` is `"binary"`, the response will be an MP3 file in binary format.

#### Example Request (base64 format):
```json
{
  "text": "ini adalah teks panjang yang akan diubah menjadi audio.",
  "output_format": "base64"
}
```

#### Example Response (base64 format):
```json
{
  "audio_base64": "<base64_encoded_audio_data>"
}
```

#### Example Request (binary format):
```json
{
  "text": "ini adalah teks panjang yang akan diubah menjadi audio.",
  "output_format": "binary"
}
```

#### Example Response (binary format):
- The response will be an MP3 file directly streamed as a binary response.

## Customization

- **Private TikTok TTS API**: This project uses a **private API** that TikTok uses internally for generating text-to-speech audio. You can modify the `generate_audio` function to point to a different TTS API or service if needed.
- **Chunk Size**: Text is split into 280-character chunks. You can adjust this value in the `split_text_into_chunks` function.

## Error Handling

- If an invalid output format is provided, the API will return a `400 Bad Request` error with a message indicating that the output format must be either "base64" or "binary".
- If there is an issue with generating the audio, the API will return a `500 Internal Server Error`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project uses an **unofficial and private API** from **TikTok** for converting text to speech. This API was obtained via **reverse engineering**, and TikTok does not provide any public documentation for it. As such:

- Use of this API **may violate TikTok’s terms of service**.
- TikTok may disable or block access to this API at any time, and there is no guarantee of the API's stability or availability.
- This project is intended for **educational purposes only**, and it is your responsibility to comply with the policies of TikTok if you use this service.
- The project author is not responsible for any misuse or violation of terms that may occur by using this API.
---

Built with ❤️ using [FastAPI](https://fastapi.tiangolo.com/).
