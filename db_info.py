from sqlalchemy import create_engine, inspect,text,MetaData
import os
from csvtodb import get_db
def create_dbengine(database_choice,db_filename=None):
    # ---> change for db_filename not = None
    try:  
          
        db_uri=""   
        current_dir = os.getcwd()
        
        if database_choice==1:
            if db_filename==None:
                db_filename='chinook.db'
            # elif db_filename.endswith('csv'):
            #     db_filename=get_db(db_filename)    
            db_path = os.path.join(current_dir, db_filename)
            
            db_uri="sqlite:///"+db_path
            # db_uri="sqlite:////home/Sravan/Desktop/d/prjcode/chinook.db"
           
        elif database_choice==2:
            
            db_uri= "postgresql://tempuser:password@localhost:5432/hrdata"
            # db_uri= "postgresql://postgres:3033@localhost:5432/hrdata"
        engine= create_engine(db_uri)
        
        return engine
    except Exception as e:
        print("sqlalchemy engine error: ",e)

def get_relations(engine):
    
    metadata = MetaData()
    metadata.reflect(bind=engine)
    relations= ""
    for table_name, table in metadata.tables.items():
        for fk in table.foreign_key_constraints:
            local_columns = ", ".join(str(column) for column in fk.columns)
            referenced_table = fk.elements[0].column.table
            referenced_columns = ", ".join(str(column) for column in referenced_table.primary_key)
            # print(f"{table_name}.{local_columns} = {referenced_table.name}.{referenced_columns}")
            # print(f"{local_columns} = {referenced_columns}")
            relations=relations+"# "+f"{local_columns} = {referenced_columns}"+'\n'
    return relations       
        
def get_table_info(database_choice,db_filename):
    try:
        if db_filename:
            if db_filename.endswith('csv'):
                db_filename=get_db(db_filename)
        if database_choice==1:
            engine=create_dbengine(database_choice,db_filename)
        elif database_choice==2:
            engine=create_dbengine(database_choice)    
        inspector = inspect(engine)
        relations=""
        relations=get_relations(engine)
        connection=engine.connect()
        table_names = [i for i in inspector.get_table_names() if not i.startswith('sql')]
        # table_names = [i for i in inspector.get_table_names() ]
        
        table_info,table_shape = {},{}


        for table_name in table_names:
            column_details = inspector.get_columns(table_name)
            columns = [column['name'] for column in column_details]
                # to get datatype of columns--> data_type=column['type']
            if table_name not in table_info:
                table_info[table_name]=columns
                
            count_query = f'SELECT COUNT(*) FROM {table_name}'
            
            num_rows = connection.execute(text(count_query)).scalar()
            if table_name not in table_shape:
                table_shape[table_name]=f"{num_rows} rows x {len(columns)} columns"   
        # print(table_shape)
        connection.close()       
        engine.dispose()
        return table_names,table_info,relations


    except Exception as e:
        print(f"table info Error: {e}")
        return None


# print(table_names,table_info)
def get_formatted_schema(database_choice=1,db_filename=None):
    
    table_names,table_info,relations=get_table_info(database_choice,db_filename)
    formatted_schema=""
    
    start_string=""
    for table_name in table_names:
        start_string="# "+table_name+" ( "
        for column in table_info[table_name]:
            
            start_string=start_string+column+", "
            
        start_string=start_string[:-2]+" )"
        formatted_schema=formatted_schema+ start_string+"\n"
    formatted_schema=formatted_schema+relations   
    # print(formatted_schema)

    return formatted_schema


