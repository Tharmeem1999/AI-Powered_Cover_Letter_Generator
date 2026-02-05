# AI-Powered Cover Letter Generator

A Streamlit application that generates hyper-personalized cover letters by analyzing job descriptions from career page URLs and matching them with your specific portfolio projects.

**🔴 [Live Demo](https://ai-powered-cover-letter-generator.onrender.com)** (Hosted on Render)

> **Note:** The live demo is currently tailored to my specific background (Data Science/AI). To use this for your own profile, please follow the "How to Customize" section below.

## How It Works

1.  **Input:** User provides a URL to a job posting (e.g., from a company career page).
2.  **Extraction:** The tool scrapes the website content using `LangChain` and `WebBaseLoader`.
3.  **Analysis:** It utilizes **Llama 3.3 (via Groq)** to extract key job requirements (Role, Experience, Skills).
4.  **Matching:** It queries a vector database (`ChromaDB`) to find the most relevant projects from your portfolio that match the job's required skills.
5.  **Generation:** The LLM generates a personalized cover letter that highlights your specific qualifications and links to your relevant portfolio projects.

## Tech Stack

* **Python 3.10+**
* **Streamlit:** Frontend UI.
* **LangChain:** Framework for LLM orchestration.
* **Groq API:** Fast inference for Llama 3.3-70b.
* **ChromaDB:** Vector store for portfolio matching.

## Project Structure

```text
CoverLetterGenerator/
├── app/
│   ├── main.py          # Streamlit app entry point
│   ├── chains.py        # LLM chains (Extraction & Writing logic)
│   ├── portfolio.py     # Vector database management
│   ├── utils.py         # Text cleaning utilities
│   └── resource/
│       └── my_portfolio.csv  # Database of your projects
├── requirements.txt
└── README.md
```

## Setup & Installation

1. **Clone the repository**
```bash
git clone https://github.com/Tharmeem1999/Pima_Diabetes_Prediction.git
cd cover-letter-generator
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up Environment Variables** Create a `.env` file in the `app/` directory (or root, depending on your setup) and add your Groq API key:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

4. **Run the App**
```bash
streamlit run app/main.py
```

## How to Customize (Make it Yours)

This project is currently set up with my personal portfolio and biographical details. If you want to clone this project to generate cover letters for **yourself**, you must update the following two files:

1. **Update Your Portfolio** (`app/resource/my_portfolio.csv`)

The `portfolio.py` file reads from a CSV file to find relevant projects. You need to replace the existing data with your own projects.

* Open `app/resource/my_portfolio.csv`
* Ensure the CSV has columns for **Techstack** (skills) and **Links** (portfolio URL)

2. **Update Your Bio** (`app/chains.py`)

The AI needs to know who you are to write the letter.

* Open `app/chains.py`
* Locate the `write_CoverLetter` method
* Find the `prompt_coverletter` variable
* **Action**: Rewrite the text inside the prompt to reflect your name, degree, university, and career goals.

**Example Change**: *Current:*
```Python
"You are Tharmeem Puthra, a recent BSc graduate from the University of Colombo..."
```

*Change to:*
```Python
"You are [Your Name], a software engineer with 5 years of experience in..."
```

## Deployment (Render)

This project is ready for deployment on [Render](https://render.com/)

1. Create a **Web Service** connected to your GitHub repo.
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command:**
```bash
streamlit run app/main.py --server.port=$PORT --server.address=0.0.0.0
```
4. **Environment Variables**: Add `GROQ_API_KEY` in the Render dashboard.

## Screenshot
<img width="1887" height="451" alt="Image" src="https://github.com/user-attachments/assets/78cb70f1-3b2a-4c0f-8f00-d6298672006f" />

