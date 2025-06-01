#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import asyncio
from openai import AsyncOpenAI, AuthenticationError, APITimeoutError, APIConnectionError
from openai.helpers import LocalAudioPlayer
from dotenv import load_dotenv

SPEECH_MODEL = "gpt-4o-mini-tts"
TRANSCRIPTION_MODEL = "gpt-4o-mini-transcribe"
# gpt-4o-mini-transcribe does not support srt format
TRANSCRIPTION_SRT_MODEL = "whisper-1"
# The voice and style used for the speech synthesis, from Brian
SPEECH_VOICE = "shimmer"
TONE_STYLE_INSTRUCTIONS = "Speak in meditative, soothing, emotive tone"
SPEECH_SPEED = 1.0


async def text_to_audio(client, text, output_filename):
    async with client.audio.speech.with_streaming_response.create(
        model=SPEECH_MODEL,
        voice=SPEECH_VOICE,
        response_format="mp3",
        speed=SPEECH_SPEED,
        input=text,
        instructions=TONE_STYLE_INSTRUCTIONS
    ) as response:
        # await LocalAudioPlayer().play(response)
        await response.stream_to_file(
            output_filename,
            chunk_size=1024
        )


async def audio_to_text(client, audio_filename):
    audio_file = await asyncio.to_thread(open, audio_filename, "rb")
    stream = await client.audio.transcriptions.create(
        model=TRANSCRIPTION_MODEL,
        file=audio_file,
        response_format="text",
        stream=True,
    )
    transcript = ""
    async for event in stream:
        if event.type == "transcript.text.delta":
            transcript += event.delta
    with open(audio_filename + '.txt', 'w') as f:
        f.write(transcript)
    audio_file.close()
    return transcript


async def audio_to_srt(client, audio_filename, max_retries=5):
    for attempt in range(max_retries):
        try:
            audio_file = await asyncio.to_thread(open, audio_filename, "rb")
            transcript = await client.audio.transcriptions.create(
                model=TRANSCRIPTION_SRT_MODEL,
                file=audio_file,
                response_format="srt"
            )
            with open(audio_filename + '.srt', 'w') as f:
                f.write(transcript)
            audio_file.close()
            return transcript
        except (AuthenticationError, APITimeoutError, APIConnectionError) as e:
            audio_file.close()
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(15 ** attempt)  # exponential backoff


def create_client():
    try:
        client = AsyncOpenAI()
        client.models.list()
        return client
    except AuthenticationError:
        print("Incorrect API")
    return None


def main():
    load_dotenv()
    client = create_client()
    # asyncio.run(audio_to_text(client, "inputs/GEN1.mp3"))

    # Traverse all folders under inputs/audios
    input_dir = "inputs/audios"
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.mp3')):  # Add more audio extensions if needed
                audio_file = os.path.join(root, file)
                print(f"Processing {audio_file}...")
                asyncio.run(audio_to_srt(client, audio_file))

    # with open("inputs/GEN1.mp3.txt", "r") as f:
    #     text = f.read()
    # asyncio.run(text_to_audio(client, text, "outputs/GEN1_new.mp3"))


if __name__ == "__main__":
    main()
