import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

st.title('Mandala Art Generator')
st.write('Generate beautiful Mandala Art based on your input.')

# Get user input
user_input = st.text_input('Enter a description for the Mandala Art')

if st.button('Generate Mandala Art'):
    if user_input:
        with st.spinner('Generating Mandala Art...'):
            # Use OpenAI API to generate Mandala Art description
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Create a detailed description of a Mandala Art based on the following input: {user_input}",
                max_tokens=200
            )
            mandala_description = response.choices[0].text.strip()
            
            st.write('Mandala Art Description:')
            st.write(mandala_description)
            
            # Displaying generated art (assuming it's a textual description or URL to an image)
            st.image("https://via.placeholder.com/300")  # Placeholder for actual art generation
    else:
        st.warning('Please enter a description for the Mandala Art.')
