import configparser

def settingUp():
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
    config['DEFAULT'] = {'DATABASE_TYPE': 'Replace',
                        'DBAPI': 'Replace',
                        'HOST': 'Replace',
                        'USER': 'Replace',
                        'PASSWORD': 'Replace',
                        'DATABASE': 'Replace',
                        'PORT': 'Replace'}
    with open('sqlconfig.ini', 'w') as configfile:
        config.write(configfile)



