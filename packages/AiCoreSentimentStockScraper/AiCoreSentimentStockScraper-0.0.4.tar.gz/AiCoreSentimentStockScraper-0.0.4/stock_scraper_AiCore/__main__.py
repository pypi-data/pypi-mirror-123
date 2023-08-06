from .config import settingUp
import configparser
import os.path
import getpass

def sqlCreds(DATABASE_TYPE,DBAPI,HOST,USER,PASSWORD,DATABASE,PORT):
    '''
    This function uses the parameters set by user to connect to PGadmin database

    The purpose of this function is to get the correct parameters and credentials
    from the user to connect to PGAdmin 4 sql data base via sqlalchamy engine. The
    function uses the data provided by the user and creates a .ini file named sqlconfig.ini

    The values for the parameters can be found on pgAdmin 4. Most of them are under properties.
    Hints: 
        DATABASE_TYPE: Server type on pgAdmin 4 (all lower case)
        DBAPI: psycopg2
        HOST: Host name / address on pgAdmin 4 
        USER: Username on pgAdmin 4
        PASSWORD: Password created by user when setting up pgAdmin 4
        DATABASE: The name of the database under Databases in pgAdmin 4
        PORT: Port in pgAdmin 4

    Output:
        .ini file contained the paremeters and credentials 
    '''

    config = configparser.ConfigParser()
    config['DEFAULT'] = {'DATABASE_TYPE': DATABASE_TYPE,
                        'DBAPI': DBAPI,
                        'HOST': HOST,
                        'USER': USER,
                        'PASSWORD': PASSWORD,
                        'DATABASE': DATABASE,
                        'PORT': PORT}
    with open('sqlconfig.ini', 'w') as configfile:
        config.write(configfile)


print('Welcome to stock scraper')
print('Lets begin...')
print('Checking if config file is populated')
requiredFields = []
config_parser = configparser.ConfigParser()
settingUp()
config_parser.read('sqlconfig.ini')
DATABASE_TYPE = config_parser['DEFAULT']['DATABASE_TYPE']
DBAPI = config_parser['DEFAULT']['DBAPI']
HOST = config_parser['DEFAULT']['HOST']
USER = config_parser['DEFAULT']['USER']
PASSWORD = config_parser['DEFAULT']['PASSWORD']
DATABASE = config_parser['DEFAULT']['DATABASE']
PORT = config_parser['DEFAULT']['PORT']
configValues = ['DATABASE_TYPE','DBAPI','HOST','USER','PASSWORD','DATABASE','PORT']
configParameters = [DATABASE_TYPE,DBAPI,HOST,USER,PASSWORD,DATABASE,PORT]
counter = 0 
for parameters in configParameters:
    if parameters=='Replace':
        requiredFields.append(configValues[counter])
    counter = +1
if not requiredFields:
    print('Config file has been populated')
    print('Starting scraper')
    from .process import stockData,stockHeadlineData,sentimentData

    # Declaring datatable names
    dt_stockContent = "stock_content"
    dt_headlines = "stock_headlines"
    dt_sentiment = "stock_sentiment"

    stockData(stockContent_name=dt_stockContent, updateFlag=True)
    stockHeadlineData(headlineDatatable_name = dt_headlines, stockInfoDatatable_name = dt_stockContent, updateFlag = True)
    sentimentData(sentimentDatatable_name=dt_sentiment, updateFlag=True, headlineDatatable_name=dt_headlines)
    print('Scraping complete')
else:
    print('Config file has NOT been populated')
    print('PGAdmin credentials required to proceed')
    credsQuestion = input('Would you like to Enter credentials now?(y/n)')
    if credsQuestion == 'y':
        print('Please enter the value for the following parameters')
        DATABASE_TYPE = input('DATABASE_TYPE: ')
        DBAPI = input('DBAPI: ')
        HOST = input('HOST: ')
        USER = input('USER: ')
        PASSWORD = getpass.getpass('PASSWORD: ')
        DATABASE = input('DATABASE: ')
        PORT = input('PORT: ')
        sqlCreds(DATABASE_TYPE=DATABASE_TYPE.strip(), DBAPI=DBAPI.strip(),HOST=HOST.strip(),USER=USER.strip(),PASSWORD=PASSWORD.strip(),DATABASE=DATABASE.strip(),PORT=PORT.strip())

        from .process import stockData,stockHeadlineData,sentimentData

        # Declaring datatable names
        dt_stockContent = "stock_content"
        dt_headlines = "stock_headlines"
        dt_sentiment = "stock_sentiment"

        stockData(stockContent_name=dt_stockContent, updateFlag=True)
        stockHeadlineData(headlineDatatable_name = dt_headlines, stockInfoDatatable_name = dt_stockContent, updateFlag = True)
        sentimentData(sentimentDatatable_name=dt_sentiment, updateFlag=True, headlineDatatable_name=dt_headlines)
        print('Scraping complete')
    else:
        print('You did not select y')
        print('Please populate congig.py file and re-run the code')
        print('The code is now exiting...')
        print('Scraping complete')

