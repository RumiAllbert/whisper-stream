import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import streamlit as st


@st.cache_resource
def initialize_pipe(model_id: str, torch_dtype: torch.dtype, device: str) -> pipeline:
    """
    Initializes the pipeline for automatic speech recognition.

    Args:
        model_id (str): The identifier of the pre-trained model.
        torch_dtype (torch.dtype): The torch data type to use.
        device (str): The device to run the model on.

    Returns:
        pipeline: The initialized pipeline for automatic speech recognition.
    """
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )

    return pipe
