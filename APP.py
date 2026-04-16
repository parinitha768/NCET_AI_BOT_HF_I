import streamlit as st
import requests

st.set_page_config("PragyanAI Image Generator", layout="wide")
st.title("PragyanAI – Text to Image Generator")

# Logo (optional)
try:
    st.image("PragyanAI_Transperent.jpg")
except:
    st.warning("Logo not found")

# User Inputs
prompt = st.text_input("Enter your image prompt")

style = st.selectbox(
    "Select Style",
    ["Realistic", "Cartoon", "Anime", "3D Render", "Digital Art"]
)

size = st.selectbox(
    "Image Size",
    ["512x512", "768x768", "1024x1024"]
)

# API Config (Example: Together AI / Stable Diffusion)
API_KEY = st.secrets["IMAGE_API_KEY"]
API_URL = "https://api.together.xyz/v1/images/generations"

# Generate Image
if st.button("Generate Image"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        try:
            full_prompt = f"""
            Create a high-quality {style} image.

            Description: {prompt}

            Highly detailed, vibrant colors, professional composition.
            """

            with st.spinner("Generating image..."):
                response = requests.post(
                    API_URL,
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "prompt": full_prompt,
                        "model": "stabilityai/stable-diffusion-xl-base-1.0",
                        "steps": 30,
                        "n": 1,
                        "size": size
                    }
                )

                data = response.json()

                # Extract image URL
                image_url = data["data"][0]["url"]

                st.session_state.image_url = image_url

                st.image(image_url, caption="Generated Image", use_column_width=True)

        except Exception as e:
            st.error(f"Error: {e}")

# Download Option
if "image_url" in st.session_state:
    try:
        img_data = requests.get(st.session_state.image_url).content

        st.download_button(
            label="⬇️ Download Image",
            data=img_data,
            file_name="generated_image.png",
            mime="image/png"
        )
    except:
        st.warning("Could not download image")

else:
    st.info("Generate an image first")
