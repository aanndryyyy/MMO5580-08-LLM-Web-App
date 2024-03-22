import streamlit as st
from langchain import PromptTemplate
#from langchain.llms import OpenAI #so vananenud rida ning asendatud allolevaga
from langchain_community.llms import OpenAI
import os

template = """
You are a seasoned nutritionist with 15 years of experience. You are crafting a customized meal plan that takes into account the client's dietary preferences and health conditions;
    MEAL PLAN input text: {content};
    CLIENT'S dietary preference: {diet};
    CLIENT'S health condition: {condition};
    TASK: Create a meal plan description that is tailored to the client's dietary preference and health condition. Incorporate specific dietary considerations into the language used;
    FORMAT: Present the result in the following order: (MEAL PLAN DESCRIPTION), (BENEFITS), (USE CASE);
    MEAL PLAN DESCRIPTION: Describe the meal plan in 5 sentences, focusing on how it caters to the dietary preference and health condition;
    BENEFITS: In 3 sentences, explain why this meal plan is ideal given the client's dietary preference and health condition;
    USE CASE: Narrate a story in 5 sentences about a day in the life of someone following this meal plan, considering {diet} and {condition}, write from a first-person perspective, for example, "I started my Monday feeling energized with ...";
"""

prompt = PromptTemplate(
    input_variables=["diet", "condition", "content"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(model_name='gpt-3.5-turbo-instruct', temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Customer tailored content", page_icon=":robot:")
st.header("Personaliseeritud turundusteksti konverter")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Otstarve: tootetutvustustekstide personaliseerimine igale kliendile või kliendigruppidele; väljundtekst on kohandatud kliendi a) vanuserühmaga ja b) hobbitegevusega; sisendtekstiks on neutraalses vormis tootekirjeldus. \
    \n\n Kasutusjuhend: 1) valmista ette tootekirjeldus (sisendtekst). 2) määra tarbijasegemendid lähtuvalt vanuserühma ja hobbide kombinatsioonidest. 3) sisesta ükshaaval tarbijasegmentide lõikes eeltoodud info äpi kasutajaliideses, saada ära. \
    4) kopeeri ükshaaval tarbijasegmentide lõikes äpi väljundteksti kõnealuse toote tutvustuslehele.")

with col2:
    st.image(image='companylogo.jpg', caption='Natural and healthy shirts for everybody')

st.markdown("## Enter Your Content To Convert")

def get_api_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        return openai_api_key
    # If OPENAI_API_KEY environment variable is not set, prompt user for input
    input_text = streamlit.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_diet = st.selectbox(
        'Toitumiseelistus',
        ('Vegan', 'Taimetoitlane', 'Segatoitlane', 'Paleo', 'Keto', 'Gluteenivaba', 'Laktoosivaba'))
    
def get_condition():
    input_text = st.text_input(label="Terviseseisund", key="condition_input")
    return input_text

condition_input = get_condition()

def get_text():
    input_text = st.text_area(label="Retsepti või toitumiskava kirjeldus", label_visibility='collapsed', placeholder="Your content...", key="content_input")
    return input_text

content_input = get_text()

if len(content_input.split(" ")) > 700:
    st.write("Please enter a shorter content. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.content_input = "t shirts, all clolors, cotton, responsible manufacturing"

st.button("*GENERATE TEXT*", type='secondary', help="Click to see an example of the content you will be converting.", on_click=update_text_with_example)

st.markdown("### Your customer tailored content:")

if content_input:
#    if not openai_api_key:
#        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
#        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_content = prompt.format(diet=option_diet, condition=condition_input, content=content_input)

    formatted_content = llm(prompt_with_content)

    st.write(formatted_content)
