
# BlinkBrief: Youtube Video Summarizer Chrome Extension




## Overview

BlinkBrief is a chrome extension developed in flask framework that summarizes YouTube videos by extracting and transcribing their audio. It uses Google Generative AI to create concise, contextually accurate summaries. Users receive brief overviews in multiple languages based on configurable summary lengths.
## Video Demonstration

Here is a demonstration video of BlinkBrief:

[Watch the video](https://www.dropbox.com/s/yourfileid/yourvideo.mp4?raw=1)

## Key Features


- Transcript Extraction : Fetches manually created and auto-generated transcripts using youtube_transcript_api. Falls back to audio transcription using AssemblyAI if transcripts are not available.

- Audio Processing : Downloads audio from YouTube in MP3 format using yt_dlp, Transcribes audio to text via AssemblyAI.

- Summary Generation : Generates summaries from transcripts using Google Generative AI Model Gemini-Pro.

- Customizable Summary Length : Short, Medium, Long

- Language Support : English, Hindi
  
- Download Options : Download summary in text or pdf file

    
## Technical Stack

- Flask: Web framework for building the chrome extension API.
- youtube_transcript_api: For retrieving video transcripts.
- yt_dlp: For downloading video audio.
- AssemblyAI: For transcribing audio.
- Google Generative AI: For generating summaries.
- jsPDF: For generating PDF summaries.

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/Ronak021/BlinkBrief.git
    ```

2. **Navigate to the Project Directory**
    ```bash
    cd BlinkBrief
    ```

3. **Create a Virtual Enovironmennt**
    ```bash
    pip install -r requirements.txt

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Set Environment Variables in .env File**:
    - `GOOGLE_API_KEY`: Your Google API key for Generative AI.
    - `ASSEMBLYAI_API_KEY`: Your AssemblyAI API key.

5. **Run the Application**:
    ```bash
    python .\app.py
    ```

## Usage

1. **Upload the Extension**:
  - Open Chrome and go to `chrome://extensions/`.
  - Enable "Developer mode" using the toggle in the top right corner.
  - Click on "Load unpacked" and select the directory containing the BlinkBrief extension files.

2. **Open the Chrome Extension**:
  - Once the extension is loaded, click the BlinkBrief icon in your Chrome toolbar to summarize desired video.

3. **Configure Summary Options**:
  - Choose the desired summary length (short, medium, long) and language (English or Hindi).

4. **View and Download Summary**:
  - The extension will process the video and provide a concise summary directly within the extension’s interface.
  - Download summary in desired format once generated. 
    
## Acknowledgements

- **[Google Generative AI](https://cloud.google.com/ai)**
- **[AssemblyAI](https://assemblyai.com/)**
- **[yt_dlp](https://github.com/yt-dlp/yt-dlp)**
- **[YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)**



