import psycopg2
from sqlalchemy import create_engine, engine
import pandas as pd
import os
import sqlalchemy
import configparser
from typing import Optional
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base


class SqlDB:
    '''
    This class is used to perform SQL datbase activities

    
    '''
    def __init__(self):
        '''
        This method is used to establish the database connection

        The purpose of this method is to use the sqlconfig.ini
        file to create a connection with the database using the 
        sqlalchmy engine.
        '''
        config_parser = configparser.ConfigParser()
        config_parser.read('sqlconfig.ini')
        DATABASE_TYPE = config_parser['DEFAULT']['DATABASE_TYPE']
        DBAPI = config_parser['DEFAULT']['DBAPI']
        HOST = config_parser['DEFAULT']['HOST']
        USER = config_parser['DEFAULT']['USER']
        PASSWORD = config_parser['DEFAULT']['PASSWORD']
        DATABASE = config_parser['DEFAULT']['DATABASE']
        PORT = config_parser['DEFAULT']['PORT']
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        self.engine = engine
    
    def deleteTable(self,table_name: str):
            Base = declarative_base()
            metadata = MetaData()
            metadata.reflect(bind=self.engine)
            table = metadata.tables[table_name]
            if table is not None:
                Base.metadata.drop_all(self.engine, [table], checkfirst=True)
    
    
    def tableExists(self,table_name: str) -> Optional[bool]:
        '''
        This method checks if a table exists in a database. 

        Args:
            table_name: The name of the table to check if it exits
            in database
        
        Returns: 
            bool: True if the table exists. False if it doesnt exist
        '''
        table_exists = sqlalchemy.inspect(self.engine).has_table(table_name)

        return table_exists

    def retriveTableInfo(self,table_name: str) -> Optional[pd.DataFrame]:
        '''
        This method returns the data from a table

        Args:
            table_name: The name of the table to check if it exits
            in database

        Returns:
            Pandas dataframe: The data of the table in pandas format
        '''
        stock_db = pd.read_sql_table(table_name, self.engine)

        return stock_db
    
    def createTable(self,table_name: str,dt_contents:pd.DataFrame):
        '''
        This method creates a table in the database

        Args: 
            table_name: The name of the table to check if it exits
            in database

            dt_contents: The data to be inserted into the table        
        '''

        creatededDt = dt_contents.to_sql(table_name, self.engine, index=False)

    def appendData(self,table_name: str,dt_contents:pd.DataFrame):
        '''
        This method appends data to a table in the database

        Args: 
            table_name: The name of the table to check if it exits
            in database

            dt_contents: The data to be inserted into the table        
        '''
        dt_contents.to_sql(table_name, self.engine, if_exists='append',index=False)
    
    def getNewRows(self,source_dt: pd.DataFrame, new_dt: pd.DataFrame):
        '''
        This method checks if data from one datable exists in another

        Args: 
            source_dt: The source datatable that to be checks against 

            new_dt: The new datatable to check

        Returns:
            Pandas dataframe: Datatable with data that does not exist in source_dt
        '''

        merged_df = source_dt.merge(new_dt, indicator=True, how='outer')
        changed_rows_df = merged_df[merged_df['_merge'] == 'right_only']
        return changed_rows_df.drop('_merge', axis=1)

# db = SqlDB()
# db.deleteTable(table_name='a')


