from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.cache import InMemoryCache
import langchain
langchain.llm_cache = InMemoryCache()
general_prompt = PromptTemplate(
    input_variables=["text"],
    template="""Generate apt response for the query stated below which is delimited within back ticks
                                       ```{text}```""",
)

llm = OpenAI(temperature=0.9)

def getLLMResponse(text):
    chain = LLMChain(llm=llm, prompt=general_prompt)
    res = chain.run(text)
    return res.split("\n")[2]