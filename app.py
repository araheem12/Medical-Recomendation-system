import streamlit as st
import torch
from tqdm import tqdm
from ctransformers import AutoModelForCausalLM

# Free up VRAM before loading the model
torch.cuda.empty_cache()

# Check if CUDA is available
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def load_model():
    st.info("Loading model... Please wait.")
    model = AutoModelForCausalLM.from_pretrained(
        "TheBloke/LLaMa-7B-GGML",
        model_type="llama",
        gpu_layers=15  # Adjust based on available VRAM
    )
    return model

# Load model only once
@st.cache_resource
def get_model():
    return load_model()

model = get_model()

def generate_response(prompt):
    with tqdm(total=1, desc="Generating Response", unit="step") as pbar:
        output = model(
            prompt,
            max_new_tokens=250,
            temperature=0.3,
            top_p=0.85,
            repetition_penalty=1.2
        )
        pbar.update(1)
    return output.strip()

# Streamlit UI
st.title("Medical Chatbot using LLaMa-7B-GGML")
st.write("Ask any medical-related questions and get concise answers!")

question = st.text_input("Enter your question:", "What is Panadol used for?")

if st.button("Generate Response"):
    if question:
        with st.spinner("Generating response..."):
            response = generate_response(question)
            st.success("Response generated successfully!")
            st.write(response)

# Display GPU memory usage if CUDA is available
if torch.cuda.is_available():
    gpu_memory_used = torch.cuda.memory_allocated() / 1e9  # Convert to GB
    st.write(f"**GPU Memory Used:** {gpu_memory_used:.2f} GB")
