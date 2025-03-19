from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import linkedin_jobs_tool

load_dotenv()

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert AI agent that clearly summarizes recent AI job postings from LinkedIn."),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}")
])

tools = [linkedin_jobs_tool]

agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

query = "Provide a summary of recent AI job postings on LinkedIn from the past week."
response = executor.invoke({"query": query})

print("\n📌 AI Job Postings Summary:\n")
print(response["output"])
