
#TODO set the open AI key correctly
import openai
from llama_index import StorageContext, load_index_from_storage
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")


from llama_index import GPTSimpleKeywordTableIndex, SimpleDirectoryReader
documents = SimpleDirectoryReader('data').load_data()
index = GPTSimpleKeywordTableIndex(documents)

engine = index.as_query_engine()


#save to disk 
index.storage_context.persist(persist_dir='./cache')
#load to disk 
storage_context = StorageContext.from_defaults(persist_dir='./cache')
index = load_index_from_storage(storage_context)

question = "Describe the users path in the video games levels and what is there end goal?"

print(f"\n== QUESTION: {question}\n")
response = engine.query(question)
print(f"== RESPONSE: {response}")