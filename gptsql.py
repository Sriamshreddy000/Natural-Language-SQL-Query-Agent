import os
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.callbacks import get_openai_callback
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv 
load_dotenv()

from csvtodb import get_sqlitedb
from extract_trace import get_final_trace

def initialize_agent(database_choice,db_filename,db_uri):
    
    db = SQLDatabase.from_uri(db_uri)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0)
    toolkit = SQLDatabaseToolkit(db=db,llm=llm)
    agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
) 
    return agent_executor


def get_db_uri(database_choice,db_filename=''):
    
    if db_filename.endswith('csv'):
        db_filename=get_sqlitedb(db_filename)
        
    db_uri=''
    if database_choice==1:
        
        start_str='sqlite:///'
        current_dir = os.getcwd()
        db_filename=db_filename or 'salesdatasample.db'    
        db_path = os.path.join(current_dir, db_filename)
        # default_db_uri = "sqlite:////home/Sravan/Desktop/d/prjcode/demo.db"
        db_uri=start_str+db_path
        
    elif database_choice==2:
        
        db_username='tempuser'
        password='password'
        host='localhost'
        port=5432
        db='hrdata'
        start_str='postgresql+psycopg2://'
        db_uri=f'{start_str}{db_username}:{password}@{host}:{port}/{db}'
        # default_db_uri="postgresql+psycopg2://tempuser:password@localhost:5432/hrdata"
        
        
    return db_uri

def get_nl_response(input_query,database_choice,db_filename=''):
   
    #change for contents not there in database ,i dont knw
    db_uri=get_db_uri(database_choice,db_filename)
    agent_executor=initialize_agent(database_choice,db_filename,db_uri)
    try:
        with get_openai_callback() as cost:
            final_answer=agent_executor.run(input=input_query,handle_parsing_errors=True)
        if final_answer==" I don't know.":
            return {'Answer':"Relevant information is not contained in the database.",'SQL':'','Result':'','Thought':'','Cost':cost}
    except ValueError:
        print("Relevant information does not exist in this database.")
        exit()
        
    sql_query,db_result,thought=get_final_trace()
    final_trace={'SQL':sql_query+';','Result':db_result,'Thought':thought,'Answer':final_answer,'Cost':cost}
    
    return final_trace

query="what type of information is present in the database?"    
# query='What are job roles of the employees and also their names, who has the top 4 salaries?'
# query='Which customer ordered the most and how many orders by that customer?'
for key,value in get_nl_response(query,1).items():
    print(f"{key}: {value}")
    