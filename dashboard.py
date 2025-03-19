import streamlit as st
from tools import scrape_linkedin_jobs
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

st.title("🚀 AI Job Market Dashboard")

# Sidebar clearly defined
job_query = st.sidebar.text_input("🔍 Job Query", "Artificial Intelligence")
days_posted = st.sidebar.slider("📅 Days since posted", 1, 14, 7)

if st.button("Fetch and Summarize Jobs"):

    with st.spinner("🔎 Fetching jobs..."):
        jobs = scrape_linkedin_jobs(job_query, days_posted)

        if not jobs or isinstance(jobs, str):
            st.error("⚠️ No jobs found or scraping error.")
        else:
            llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

            # Direct and simplified prompt clearly defined without agent_scratchpad
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Clearly and concisely summarize these LinkedIn job postings."),
                ("human", "{query}")
            ])

            # Format job details
            job_details = "\n\n".join(
                [f"{j['title']} at {j['company']} ({j['location']})\nLink: {j['link']}" for j in jobs]
            )

            query = f"Summarize these recent AI job listings:\n\n{job_details}"

            with st.spinner("🤖 Summarizing with AI..."):
                chain = prompt | llm
                response = chain.invoke({"query": query})

            st.subheader("📌 AI-Generated Job Summary")
            st.markdown(response.content)

            st.subheader("📑 Detailed Listings")
            for job in jobs:
                st.markdown(f"### [{job['title']}]({job['link']})")
                st.write(f"**Company:** {job['company']}")
                st.write(f"**Location:** {job['location']}")
                st.write(f"**Posted:** {job['date_posted']}")
                st.markdown("---")
