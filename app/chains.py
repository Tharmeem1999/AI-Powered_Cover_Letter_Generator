import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()       # loads API keys from .env file

class Chain:
    def __init__(self):
        # sets up LLM with groq API. uses Llama 3.3
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        # template to extract structured job data from scraped career page
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `Company name`, `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm  # chains prompt + LLM together
        res = chain_extract.invoke(input={"page_data": cleaned_text})  # runs LLM on cleaned text
        try:
            json_parser = JsonOutputParser()  # parses LLM output into JSON
            res = json_parser.parse(res.content)
        except OutputParserException:
            # handles case where LLM output is too long or malformed
            raise OutputParserException("Context too big. Unable to parse jobs.")
        # ensures return is always a list (even if one job) for consistent iteration
        return res if isinstance(res, list) else [res]

    def write_CoverLetter(self, job, links):
        # template to generate a cover letter using job data + portfolio links
        prompt_coverletter = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Tharmeem Puthra, a recent BSc graduate from the University of Colombo. Your modules focused on Statistics, 
            Mathematics, and Computer Science. You have also participated in university hackathons and are a member of the 
            Mathematics & Statistics Research Circle. You are currently pursuing an MSc in Data Science and AI from the University 
            of Moratuwa. Data Science and AI is the field you are most interested in. You are actively seeking an internship, 
            trainee, or entry-level job opportunity in industry.

            Your job is to write a cover letter for the company's hiring team regarding the job mentioned above. Describe your 
            capabilities and how they fit the role's skills requirements. Also include the most relevant portfolio items from: 
            {link_list}

            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )

        chain_coverletter = prompt_coverletter | self.llm  # chains cover letter prompt + LLM
        res = chain_coverletter.invoke({"job_description": str(job), "link_list": links})  # generates cover letter
        return res.content  # returns only cover letter body