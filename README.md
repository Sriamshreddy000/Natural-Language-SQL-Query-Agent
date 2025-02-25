# Natural-Language-SQL-Query-Agent

Requirements:
langchain==0.0.311
openai==0.27.10
pandas==2.1.1
psycopg2_binary==2.9.7
python-dotenv==1.0.0
Requests==2.31.0
SQLAlchemy==1.4.39
streamlit==1.27.0
streamlit_chat==0.1.1
streamlit_extras==0.3.4

Evaluation metrics:
Evaluating the performance of Text-to-SQL systems is a critical aspect of understanding their effectiveness and practical applicability.It helps identify the accuracy/performance of the system  in converting diverse natural language queries into semantically correct SQL expressions.The evaluation of a generated query by a Text-to-SQL system commonly entails comparing it to a ground truth query, often referred to as gold SQL.Evaluation metrics can be classified into three types --string matching, execution matching and manual evaluation.

String matching
Exact match:
Exact String Match is the strictest metric. It demands an exact match between the generated  query and the reference gold SQL, right down to every character and a match is found only when generated query is same as ground truth SQL. This includes the order of clauses , aliases  and even the formatting used.It is widely used to evaluate the Text to sql systems  especially by rule-based and Template-based approaches where a predefined structure is to be followed.However its strictness in exact string matching can be a drawback.An SQL query can be constructed in ways  that differ in syntactical structure but produce semantically equivalent results.This makes Exact String matching unsuitable for deep learning approaches that emphasize flexibility in query construction.

Execution Match:
In contrast to exact-match methods that directly compare structural components or strings in the output, execution match assesses the correctness of a semantic expression based on results obtained after execution against the database. If the results align, the generated query is deemed correct, irrespective of syntactic differences with the gold SQL. This metric is particularly valuable in scenarios where distinct query expressions may produce the equivalent desired output.However
a drawback of this metric is the potential for false positives, where two queries, despite yielding identical results, exhibit differences at a semantic level.  For example, when both queries return empty results or when conditinal filtering is applied to distinct columns, coincidentally resulting in the same outcome.

Manual Evaluation:
Manual evaluation involves human evaluators assessing the generated SQL queries to determine how effectively they capture the user's intent.
Human evaluation plays a crucial role in identifying the nuanced aspects of semantic equivalence, especially in situations where the execution results of two expressions may differ, yet both are valid in real-world contexts. Consider restaurant-related queries where both SELECT name FROM restaurants WHERE cuisine = "Italian" and SELECT id, name FROM restaurants WHERE cuisine = "Italian" could be recognized as valid responses when inquiring about Italian cuisine establishments, even though they result in different outputs.Although manual evaluation provides in-depth insights, it is a labor-intensive and time-consuming process, and the subjective nature of evaluators can impact the results.Therefore, manual evaluation is often used alongwith automatic evaluation metrics for comprehensive evaluation.
