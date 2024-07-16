import streamlit as st
from openai import OpenAI

api_key = st.secrets['OPENAI_SECRET']

# Statics

# Methods
def generate_story_line(prompt, client, background_theme):
  story_response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{
        "role": "system",
        "content": f"You're a bestseller story writer. You will take user's prompt and generate a 100 words short story for adults age 20-30 with the background of {background_theme}"
    }, {
        "role": "user",
        "content": f"{prompt}"
    }],
    max_tokens=400,
    temperature=0.8
  )
  return story_response.choices[0].message.content


def refine_story_for_cover(story_line, client):
  design_response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{
        "role": "system",
        "content": """
        Based on the story given. You will design the detailed image prompt for the cover of this story. The image prompt should include the theme of the story with relevant color that si suitable for adults.
        The output should be within 100 characters.
        """
    }, {
        "role": "user",
        "content": f"{story_line}"
    }],
    max_tokens=400,
    temperature=0.8

  )
  return design_response.choices[0].message.content

def generate_cover(image_prompt, client, color_theme):
    cover_response = client.images.generate(
        model='dall-e-2',
        prompt=f"{image_prompt} with the color theme of {color_theme} that is in ghibili theme.",
        size='256x256',
        quality='standard',
        n=1
    )
    
    return cover_response.data[0].url

# Set up OpenAI API credentials
client = OpenAI(api_key=api_key)

st.title("Story Book Cover Generator")



with st.form("storybook_form"):
    st.write("Information for your storybook")

    background_theme = st.selectbox('Select Background:', ["Jungle", "Marine", "Beach", "Space", "Desert", "Forest"])
    
    color_theme = st.selectbox('Select Color Theme:', ["Warm", "Cold", "Neutral"])

    prompt = st.text_input(label="Some keywords to generate a story:")

    submitted = st.form_submit_button('Submit preferences')

    if submitted:
        st.write("Generating storybook...")
        story = generate_story_line(prompt, client, background_theme)
        cover_prompt = refine_story_for_cover(story, client)
        image_url = generate_cover(cover_prompt, client, color_theme)
        st.image(image_url)
        st.write(story)

