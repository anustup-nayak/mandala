import streamlit as st
import requests
import os
from PIL import Image
from io import BytesIO
import base64
# No openai import needed as we're using requests directly

# Set page configuration
st.set_page_config(
    page_title="Mandala Art Generator",
    page_icon="🔮",
    layout="centered"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #3498db;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 2rem;
        text-align: center;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    .result-header {
        font-size: 1.75rem;
        color: #2c3e50;
        margin: 1.5rem 0;
        text-align: center;
    }
    .download-section {
        text-align: center;
        margin-top: 1rem;
    }
    .footnote {
        font-size: 0.8rem;
        color: #7f8c8d;
        text-align: center;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown("<h1 class='main-header'>✨ Mandala Art Generator ✨</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Create beautiful mandala art with AI</p>", unsafe_allow_html=True)

# Function to generate mandala using OpenAI API
def generate_mandala(api_key, style, color_scheme, complexity, custom_elements):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Build the prompt
    prompt = f"A beautiful {complexity} {style} mandala with {color_scheme} colors"
    if custom_elements:
        prompt += f", incorporating {custom_elements}"
    prompt += ". Perfect symmetry, intricate details, centered composition, professional artwork."
    
    # For debugging
    st.session_state['last_prompt'] = prompt
    
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "standard",
        "response_format": "url"
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            image_url = data["data"][0]["url"]
            return image_url, None
        else:
            error_data = response.json()
            error_message = error_data.get("error", {}).get("message", "Unknown error occurred")
            return None, error_message
    
    except Exception as e:
        return None, str(e)

# Function to get image data for download
def get_image_download_link(img_url, filename="mandala.png"):
    response = requests.get(img_url)
    image = Image.open(BytesIO(response.content))
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">Download Mandala Image</a>'
    return href

# Sidebar for API key
with st.sidebar:
    st.header("🔑 API Settings")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    st.caption("Your API key is used only in this session and is not stored.")
    
    # Show help/information
    with st.expander("ℹ️ Need an API Key?"):
        st.write("1. Visit [OpenAI Platform](https://platform.openai.com/)")
        st.write("2. Sign up or log in to your account")
        st.write("3. Navigate to API Keys section")
        st.write("4. Create a new secret key")
        st.write("Note: API usage will incur charges to your OpenAI account")

# Main form
st.header("🎨 Customize Your Mandala")

col1, col2 = st.columns(2)

with col1:
    style = st.selectbox(
        "Mandala Style",
        ["Geometric", "Floral", "Spiritual", "Celtic", "Abstract", "Tribal", "Futuristic"]
    )
    
    complexity = st.select_slider(
        "Complexity",
        options=["Simple", "Moderate", "Complex", "Intricate"],
        value="Moderate"
    )

with col2:
    color_scheme = st.radio(
        "Color Scheme",
        ["Colorful", "Monochrome", "Pastels", "Vibrant", "Earth tones"]
    )
    
    custom_elements = st.text_area(
        "Additional Elements (optional)",
        placeholder="E.g., lotus flowers, sacred geometry, animal motifs...",
        max_chars=100
    )

# Generation section
st.header("🔮 Generate Your Mandala")

if 'generated_image' not in st.session_state:
    st.session_state['generated_image'] = None
    st.session_state['last_prompt'] = ""

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("Generate Mandala", use_container_width=True):
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar.")
        else:
            with st.spinner("Creating your mandala... This may take up to 30 seconds."):
                image_url, error = generate_mandala(
                    api_key,
                    style.lower(),
                    color_scheme.lower(),
                    complexity.lower(),
                    custom_elements
                )
                
                if error:
                    st.error(f"Error: {error}")
                else:
                    st.session_state['generated_image'] = image_url

# Display the generated image
if st.session_state['generated_image']:
    st.markdown("<h2 class='result-header'>🌟 Your Mandala 🌟</h2>", unsafe_allow_html=True)
    st.image(st.session_state['generated_image'], caption="Generated Mandala", use_column_width=True)
    
    # Download section
    st.markdown("<div class='download-section'>", unsafe_allow_html=True)
    st.markdown(get_image_download_link(st.session_state['generated_image']), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Option to view the prompt used
    with st.expander("View prompt used to generate this mandala"):
        st.write(st.session_state['last_prompt'])

# Footer
st.markdown("<p class='footnote'>This app uses OpenAI's DALL-E API to generate images. Usage is subject to OpenAI's terms of service.</p>", unsafe_allow_html=True)
