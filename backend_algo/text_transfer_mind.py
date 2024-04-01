from backend_algo.config import *

from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.callbacks import get_openai_callback



prompt_template_mindmap = """

You are an experienced assistant in helping people understand topics through the help of mind maps.

You are an expert in the field of the requested topic.

Make a mindmap based on the context below. Try to make connections between the different topics and be concise.:

------------
{text}
------------

Think step by step.

Always answer in markdown text. Adhere to the following structure:

## Main Topic 1

### Subtopic 1
- Subtopic 1
    -Subtopic 1
    -Subtopic 2
    -Subtopic 3

### Subtopic 2
- Subtopic 1
    -Subtopic 1
    -Subtopic 2
    -Subtopic 3

## Main Topic 2

### Subtopic 1
- Subtopic 1
    -Subtopic 1
    -Subtopic 2
    -Subtopic 3

Make sure you only put out the Markdown text, do not put out anything else. Also make sure you have the correct indentation.


MINDMAP IN MARKDOWN:

"""


# Template for refining the mindmap

refine_template_mindmap = ("""

You are an experienced assistant in helping people understand topics through the help of mind maps.

You are an expert in the field of the requested topic.

We have received some mindmap in markdown to a certain extent: {existing_answer}.
We have the option to refine the existing mindmap or add new parts. Try to make connections between the different topics and be concise.
(only if necessary) with some more context below
"------------\n"
"{text}\n"
"------------\n"


Always answer in markdown text. Try to make connections between the different topics and be concise. Adhere to the following structure:

## Main Topic 1

### Subtopic 1
- Subtopic 1
    -Subtopic 1
    -Subtopic 2
    -Subtopic 3

### Subtopic 2
- Subtopic 1
    -Subtopic 1
    -Subtopic 2
    -Subtopic 3

## Main Topic 2

### Subtopic 1
- Subtopic 1
    -Subtopic 1
    -Subtopic 2
    -Subtopic 3

Make sure you only put out the Markdown text, do not put out anything else. Also make sure you have the correct indentation.

MINDMAP IN MARKDOWN:
"""
)


def text_to_mind(text):

    # Set your OpenAI API Key.
    # openai_api_key = OPENAI_API_KEYS

    # Split Data For Mindmap Generation
    text_splitter = TokenTextSplitter(model_name=OPENAI_API_MODEL, chunk_size=10000, chunk_overlap=1000)
    texts_for_mindmap = text_splitter.split_text(text)
    docs_for_mindmap = [Document(page_content=t) for t in texts_for_mindmap]

    PROMPT_MINDMAP = PromptTemplate(template=prompt_template_mindmap, input_variables=["text"])
    REFINE_PROMPT_MINDMAP = PromptTemplate(
        input_variables=["existing_answer", "text"],
        template=refine_template_mindmap,
    )

    with get_openai_callback() as cb:

        llm_markdown = ChatOpenAI(openai_api_key=OPENAI_API_KEYS, temperature=0.3, model=OPENAI_API_MODEL)

        summarize_chain = load_summarize_chain(llm=llm_markdown, 
        chain_type="refine", verbose=False, question_prompt=PROMPT_MINDMAP, refine_prompt=REFINE_PROMPT_MINDMAP) # 

        # Generate mindmap
        mindmap = summarize_chain(docs_for_mindmap)

        # print("=========>>>>>>>>>", mindmap['output_text'])

    # Print cost
    # print(">>>>>>>>>token cost: ", cb)
    return mindmap['output_text'], cb