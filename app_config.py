from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()
prompt = PromptTemplate(
    template="""You are a management consultant with an MBA and a PhD in organisational psychology. \
    I'm going to present you with a extract of pain points \
    I want you to extract each individual painpoint and return them as a list of entities. \
    I want you to be very specific. Sometimes there will be more than one pain point in a single line.
    Extract what the pain point is for the organisation. Be very specific about the pain point.
    Each needs to be a proper sentence and it needs to tie to either a organisational pain point or a customer pain point.
    {additional_prompts}
    format them according to: {format_instructions} \
    Make sure you only return a single entity per list item.
    The values are as follows:
    {data}
    
    """,
    input_variables=["additional_prompts", "data"],
    partial_variables={"format_instructions": format_instructions}
)

model = ChatOpenAI(model_name="o1-mini", temperature=1)
