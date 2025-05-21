#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import asyncio
from openai import AsyncOpenAI, AuthenticationError
from openai.helpers import LocalAudioPlayer
from dotenv import load_dotenv

SPEECH_MODEL = "gpt-4o-mini-tts"
TRANSCRIPTION_MODEL = "gpt-4o-mini-transcribe"
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


async def transcribe_audio(client, audio_filename):
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
    asyncio.run(transcribe_audio(client, "inputs/GEN1.mp3"))
    with open("outputs/GEN1.mp3.txt", "r") as f:
        text = f.read()
    asyncio.run(text_to_audio(client, text, "outputs/GEN1_new.mp3"))


if __name__ == "__main__":
    main()
