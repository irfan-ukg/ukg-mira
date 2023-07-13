"""Main file where all the action of MIRA begins
"""
from fastapi import FastAPI, File, UploadFile, Body
from fastapi.responses import FileResponse
from services.index import processContext, processAudioContext, processAudioGenAudioFileResp
import os

mira = FastAPI()


@mira.get("/ping")
async def root():
    return {"message": "Pong! ...from MIRA"}

@mira.post("/text/chat")
async def chatHandler(body: dict =  Body(...)):
    context = body["context"]
    result = await processContext(context)
    return {"message": f"Received response from LLM is: {result}"}

@mira.post("/audio/chat")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    """Audio files couldn't be passed to whisper library as streams: https://github.com/openai/whisper/discussions/2
        Therfore, we must store the complete chunk of incoming audio byte and once we are done with the processing,
        we shall delete the file to avoid unnecessary increase in the disk space
    """
    file_location = f".data/files/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    print({"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"})
    result = await processAudioContext(file_location)
    os.remove(file_location)
    return {"message": f"Received context is: {result}"}

@mira.post("/audio/audio")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    """Audio files couldn't be passed to whisper library as streams: https://github.com/openai/whisper/discussions/2
        Therfore, we must store the complete chunk of incoming audio byte and once we are done with the processing,
        we shall delete the file to avoid unnecessary increase in the disk space
    """
    file_location = f".data/files/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    print({"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"})
    respAudioFileLocation = await processAudioGenAudioFileResp(file_location)
    os.remove(file_location)
    return FileResponse(respAudioFileLocation)


