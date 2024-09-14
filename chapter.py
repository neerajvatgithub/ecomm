import openai
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Set your OpenAI API key
openai.api_key = 'sk-proj-expOpqxZmNpZ2C0A1awgT3BlbkFJutnAo0YcByYk8phanuzY'


def extract_video_id(url):
    # Extract video ID from YouTube URL
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if video_id_match:
        return video_id_match.group(1)
    return None


def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        print(f"An error occurred while fetching the transcript: {e}")
        return None


def generate_chapters_with_llm(transcript):
    prompt = "Generate 5 concise chapter titles for the following video transcript:\n\n"
    prompt += transcript[:4000]  # Limit to first 4000 characters to fit within token limit
    prompt += "\n\nProvide 5 chapter titles in the following format:\n1. Title 1\n2. Title 2\n3. Title 3\n4. Title 4\n5. Title 5"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant that generates chapter titles for video transcripts."},
                {"role": "user", "content": prompt}
            ]
        )
        chapter_titles = response.choices[0].message['content'].strip().split('\n')
        return [title.split('. ', 1)[1] for title in chapter_titles if '. ' in title]
    except Exception as e:
        print(f"An error occurred while generating chapters: {e}")
        return []


def generate_chapters_with_timestamps(chapter_titles, video_duration):
    chapters = []
    time_interval = video_duration // len(chapter_titles)
    current_time = 0
    for title in chapter_titles:
        chapters.append((current_time, title))
        current_time += time_interval
    return chapters


def format_chapters(chapters_with_timestamps):
    formatted_chapters = []
    for timestamp, title in chapters_with_timestamps:
        minutes = timestamp // 60
        seconds = timestamp % 60
        formatted_chapters.append(f'{minutes:02}:{seconds:02} - {title}')
    return formatted_chapters


def process_youtube_video(url):
    video_id = extract_video_id(url)
    if not video_id:
        print("Invalid YouTube URL")
        return

    transcript = get_transcript(video_id)
    if not transcript:
        print("Failed to fetch transcript")
        return

    chapter_titles = generate_chapters_with_llm(transcript)

    # Assuming an average video duration of 10 minutes (600 seconds)
    # In a real scenario, you'd want to get the actual video duration
    video_duration = 1000

    chapters_with_timestamps = generate_chapters_with_timestamps(chapter_titles, video_duration)
    formatted_chapters = format_chapters(chapters_with_timestamps)

    print("Generated Chapters:")
    for chapter in formatted_chapters:
        print(chapter)


# Example usage
youtube_url = "https://www.youtube.com/watch?v=D-c7VA87RIE&t=2s"
process_youtube_video(youtube_url)