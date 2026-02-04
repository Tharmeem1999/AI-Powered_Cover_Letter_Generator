import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path      # path to .csv file
        self.data = pd.read_csv(file_path)      # loads portfolio data into dataframe
        self.chroma_client = chromadb.PersistentClient('vectorstore')       # sets up local vector DB
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")     # creates/ reuses collection

    def load_portfolio(self):
        # Only loads data if collection is empty, avoids duplicate entries
        if not self.collection.count():
            for _, row in self.data.iterrows():
                # Stores each Project as searchable doc, with GitHub link & Skills in metadata
                self.collection.add(documents=row["Project"],
                                    metadatas={"links": row["GitHub Link"], "skill": row["Skills"]},
                                    ids=[str(uuid.uuid4())])  # Unique ID for each entry

    def query_links(self, skills):
        # Searches vector DB for top 2 portfolio items matching input skills
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])