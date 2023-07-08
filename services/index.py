"""Contains the abstraction code for MIRA Brain
"""
from services.langchain.mira_llm_operations import getLLMResponse
from services.audio_processer import speechToText, textToSpeech
async def processContext(context):
    return getLLMResponse(context)

async def processAudioContext(audio_context):
    context = await speechToText(audio_context)
    return getLLMResponse(context)

async def processAudioGenAudioFileResp(audio_context):
    context = await speechToText(audio_context)
    respText = getLLMResponse(context)
    dest_audio_path = '.data/out_files/hello.wav'
    respAudioFilePath = await textToSpeech(respText, dest_audio_path)
    return respAudioFilePath
