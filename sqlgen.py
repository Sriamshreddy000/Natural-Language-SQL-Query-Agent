import re
from langchain.chat_models import ChatOpenAI
from db_info import get_formatted_schema
from dotenv import load_dotenv 
load_dotenv()


def get_formatted_llmresponse(llmresponse):
    
    matches = re.finditer(r'SELECT.*?;', llmresponse, re.DOTALL)
    sql_queries = [match.group(0).replace('\n',' ') for match in matches]
    
    return sql_queries
    
    
def get_sql_response(user_input,database_choice,db_filename=None):
    
    chat_prompt= [
    {
        "role": "system",
        "content": "You are now an excellent SQL writer, first I'll give you some tips and examples, and I need you to remember the tips, and do not make same mistakes."
    },
    {
        "role": "user",
        "content": """Tips 1: 
Question: Which A has most number of B?
Gold SQL: select A from B group by A order by count ( * ) desc limit 1;
Notice that the Gold SQL doesn't select COUNT(*) because the question only wants to know the A and the number should be only used in ORDER BY clause, there are many questions asks in this way, and I need you to remember this in the the following questions."""
    },
    {
        "role": "assistant",
        "content": "Thank you for the tip! I'll keep in mind that when the question only asks for a certain field, I should not include the COUNT(*) in the SELECT statement, but instead use it in the ORDER BY clause to sort the results based on the count of that field."
    },
    {
        "role": "user",
        "content": """Tips 2: 
Don't use "IN", "OR", "LEFT JOIN" as it might cause extra results, use "INTERSECT" or "EXCEPT" instead, and remember to use "DISTINCT" or "LIMIT" when necessary.
For example, 
Question: Who are the A who have been nominated for both B award and C award?
Gold SQL should be: select A from X where award = 'B' intersect select A from X where award = 'C';"""
    },
    {
        "role": "assistant",
        "content": "Thank you for the tip! I'll remember to use \"INTERSECT\" or \"EXCEPT\" instead of \"IN\", \"OR\", or \"LEFT JOIN\" when I want to find records that match or don't match across two tables. Additionally, I'll make sure to use \"DISTINCT\" or \"LIMIT\" when necessary to avoid repetitive results or limit the number of results returned."
    },
    
    {
        "role": "user",
        "content": """Tips 3: 
Don't provide explanation as a replacement for providing 2 similar yet different SQL queries.Also for use cases that require 'highest and least' in one query follow this example below. 
Question: Which two cities has received the highest and least number of orders respectively?"
Gold SQL should be: SELECT City, num_orders
FROM (
    SELECT City, COUNT(*) AS num_orders
    FROM salesdatasample_table
    GROUP BY City
    ORDER BY num_orders DESC
    LIMIT 1
) AS highest_orders

UNION

SELECT City, num_orders
FROM (
    SELECT City, COUNT(*) AS num_orders
    FROM salesdatasample_table
    GROUP BY City
    ORDER BY num_orders ASC
    LIMIT 1
) AS least_orders;
Notice that the Gold SQL doesn't provide 2 queries instead provides a single query using subqueries and union ,also order by clause always comes after union clause in Gold SQL.Also notice that Gold SQL doest return 2 cities from descending clause ,it returns one city each from asc and desc clause."""
    },
    {
        "role": "assistant",
        "content": "Thank you for the tip! I'll remember to use \"UNION\" and/or Sub-Queries instead of two different queries or single query that doesn't fulfill task requirements. Additionally, I'll make sure to use \"ORDER BY\" clause always after \"UNION\" clause when necessary to avoid errors and also I'll be cautious and double-check the number of opening and closing parenthesis always when using Sub-Queries."
    }
]
    db_schema=get_formatted_schema(database_choice,db_filename)
    
    user_prompt=f'''role": "user",
    "content":"""### Complete sqlite SQL query only and with no explanation, and do not select extra columns that are not
explicitly requested in the query.An SQL query must have a semicolon in the end of query.
### Sqlite SQL tables, with their properties:
#
{db_schema}
#

### {user_input}

'''
    chat_prompt.append({user_prompt})
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0)
    llm_response=llm.predict(str(chat_prompt))
    # print(llm_response)
    sql_list=get_formatted_llmresponse(llm_response)
    
    return sql_list,llm_response.replace('Gold SQL: ',"")





# code from below to be moved to frontend
user_inp='How many categories exist?'
all_sqls,llmresponse=get_sql_response(user_inp,1,'demo.db')
# all_sqls,llmresponse=get_sql_response(user_inp,2)
num_queries=len(all_sqls)
if num_queries==0:
    print("error")
    
elif num_queries==1:
    print(all_sqls[0])
    pass    
elif num_queries>1:
    for i in all_sqls:
        print(i)
