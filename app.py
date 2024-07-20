import os
from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL
import assemblyai as aai
import google.generativeai as genai
from urllib.parse import urlparse, parse_qs



application = Flask(__name__)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
aai.settings.api_key = ASSEMBLYAI_API_KEY


def get_video_id(url):
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get('v')
    return video_id[0] if video_id else None

# The overall workflow 
@application.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    language = request.args.get('language', 'en')
    summary_len = request.args.get('summaryLength', 'short')
    video_id = get_video_id(url)

    try:
        transcript, transcript_len = get_transcript(video_id)
    except Exception as e:
        return "Error: {}".format(str(e)), 404

    try:
        # print("Generating The Summary")
        summary = generate_summary(transcript,transcript_len, language, summary_len)
    except Exception as e:
        print(e)
        return "Error: {}".format(str(e)), 404

    return summary, 200



def download_audio(video_id):
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'tmp/%(id)s.%(ext)s',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        mp3_path = os.path.join("tmp/", f"{video_id}.mp3")
        
        return mp3_path
    except Exception as e:
        raise Exception(f"Error downloading audio: {e}")


def transcribe_audio(file_path):
    # print("getting the Assemlyai api key..")

    # URL of the file to transcribe
    FILE_URL = file_path

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)

    # remove mp3 file
    os.remove(file_path)

    if transcript.status == aai.TranscriptStatus.error:
        # print(transcript.error)
        return 404
    else:
        # print(transcript.text)
        return transcript.text


def get_transcript(video_id):

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id) 

        if(transcript_list):
            try:
                # print("Fetching the manual transcript...")
                transcript = transcript_list.find_manually_created_transcript()
                
            except:
                # print("Fetching the auto-generated transcript...")
                generated_transcripts = [trans for trans in transcript_list if trans.is_generated]
                transcript = generated_transcripts[0]

    except Exception as e:
        try:
            # print("Transcript/List not found on YT, Fetching using assembly ai model...")
            audio_path=download_audio(video_id) 
            text = transcribe_audio(audio_path)
            text_length = len(text.split())
            return text, text_length
        except Exception as e:
            print(f"An error occurred while retrieving transcripts:{e}")

    transcript = " ".join([part['text'] for part in transcript.fetch()])
    transcript_len = len(transcript.split())
    return transcript, transcript_len


def generate_summary(transcript, transcript_len, language, summary_len):
    print(f"The length of the Transcript : {transcript_len}")
    
    if summary_len == "short": 
        summaryLength= min(60, transcript_len)
    elif summary_len == "medium": 
        summaryLength= max(150, int(transcript_len * 0.3))
    else:
        summaryLength=max(300, int(transcript_len * 0.5))

    if language == "en":
        summaryLangauge = "English"
    elif language == "hi":
        summaryLangauge = "Hindi"
   

    print(summaryLength, summaryLangauge)

    prompt=f"""You are Youtube video summarizer. You will be taking the transcript text
    and summarizing the entire video and providing the important summary in points
    within {summaryLength} words and in {summaryLangauge} Langauge.
    **Note** That length and language convention should be **strictly** followed.
    Please provide the summary of the text given here: {transcript} """


    model=genai.GenerativeModel("gemini-pro")
    summary=model.generate_content(prompt)
  

    return summary.text

if __name__ == '__main__':
    application.run(debug=True)


