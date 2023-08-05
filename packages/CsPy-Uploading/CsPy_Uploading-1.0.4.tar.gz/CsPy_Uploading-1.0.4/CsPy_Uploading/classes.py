import pandas as pd
import numpy as np
import datetime as dt
import os as os
import humanfriendly as hf
import platform as pl
import time
import json
import pymssql
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPException
from google.cloud.bigquery import Client, LoadJobConfig, DatasetReference
from google.cloud.bigquery import SchemaField as sf
from google.oauth2 import service_account

from CsPy_Uploading.functions import left
from CsPy_Uploading.functions import right


class BaseJob:
    """
    Desc:
        BaseJob (class): Underlying Class For UploadJob and DownloadJob

    Args:
        query (str): If uploading via SQL or BQ this is the query you wish to run
              Notes: Not needed if you are uploading via a CSV, JSON or DATAFRAME data types

        bq_project (str): The name of the big query project you wish to upload to

        bq_key_path (str): The file path to the folder that your BQ service account is stored
                  Example: "C:/Users/RobinsonJa/Service_Accounts/"

        bq_key_name (str): Name of your BQ service account file
                  Example: "bq_key.json"

        sql_server (str): The connection name of the sql server you wish to read data from
                   Notes: Not needed if you are uploading via BQ, CSV, JSON or DATAFRAME
                   Notes: Not needed if you are using an account and plan on using your default server

        sql_key_path (str): The file path to the folder that your SQL service account is stored
                   Example: "C:/Users/RobinsonJa/Service_Accounts/"
                     Notes: Not needed if you are uploading via BQ, CSV, JSON or DATAFRAME

        sql_key_name (str): Name of your SQL service account file
                   Example: "sql_key.json"
                     Notes: Not needed if you are uploading via BQ, CSV, JSON or DATAFRAME
                     Notes: Not needed if you are using an account and plan on using your default key name

    Optional Args:
        input_data_from (str): Type of data that will be used in the job.
                        Notes: Accepted inputs are SQL, BQ, CSV, JSON, DATAFRAME
                        Notes: Optional but recommended argument

        save_file_path (str): The file path used to store data files for Upload or Download
                     Example: "C:/Users/RobinsonJa/data/"
                       Notes: If not supplied job will create a temporary DATA folder then is remove after upload
                       Notes: Optional but recommended argument

        account_first_name (str): First name used on the account you wish to use
                           Notes: Used to read the account details for the given first name
                           Notes: Using accounts will require less overall inputs per job

        account_surname (str): Surname used on the account you wish to use
                           Notes: Used to read the account details for the given first name
                           Notes: Using accounts will require less overall inputs per job

        account_file_path (str): The file path to the folder that your account is stored
                        Example: "C:/Users/RobinsonJa/account/"
                          Notes: Not needed if your account file is within the working directory of your script
                          Notes: Not needed on the VM if you have saved the account in the designated folder

    Setting Args:
        set_logging (bool): Set True for console output. Set False for no console output
                     Notes: Defaults to True

    Returns:
        No values are returned as this class just initialises a Job

    Raises:
        No exceptions raise in this initialisation class
    """

    def __init__(self, query=None, input_data_from=None,
                 bq_project=None, bq_key_path=None, bq_key_name=None,
                 sql_server=None, sql_key_path=None, sql_key_name=None, save_file_path=None,
                 account_first_name=None, account_surname=None, account_file_path=None,
                 set_logging=None, set_testing=None):

        # Initialisation
        self.start_time = dt.datetime.now()
        self.temp_set_logging = set_logging
        self.version = '1.0.4'
        self.run_error = False
        self.sys_exit = False
        self.thg_log()

        # Job Variables
        self.job_details = {'Table Partitions': 0,
                            'Job Progress': 'Initialising',
                            'Job Portion': 'Job Initialisation',
                            'Bytes Uploaded': '',
                            'Location On VM': '',
                            'Script Name': '',
                            'BQ Account Used': '',
                            'Error': '',
                            'Error Message': '',
                            'Solution': '',
                            'Upload Type': '',
                            'SQL Access': '',
                            'BQ Access': '',
                            'GA Error': '',
                            'Job Status': '',
                            'Date Partitioned': '',
                            'Owner': '',
                            'Run Date': self.start_time,
                            'Runtime': '',
                            'BQ Project': '',
                            'BQ Dataset': '',
                            'BQ Table': '',
                            'SQL Server': '',
                            'SQL Account': ''
                            }
        self.job_type = None

        # Setting Variables
        self.job_details['Job Progress'] = 'Initialising Settings'
        self.setting = JobSettings(set_logging, set_testing)

        # Initialising Job - Part 1: VM Status
        self.progress_update('Initialising Job', print_line=True, print_value=True)
        self.query = query
        self.input_data_from = input_data_from
        self.vm_status = False
        self.get_vm_status()

        # Initialising Job - Part 2: Account
        self.progress_update('Getting Account Details', print_line=True, print_value=True)
        self.first_name = account_first_name
        self.surname = account_surname
        self.account_file_path = account_file_path
        self.account = Account(account_first_name, account_surname, account_file_path, self.vm_status,
                               self.setting.logging)
        self.use_account = self.account.use_account

        # Initialising Job - Part 3: Save File Path
        self.save_file_path = save_file_path
        self.get_save_file_path()

        # BQ Variables
        self.progress_update('Initialising SQL Variables', print_line=False, print_value=False)
        self.bq_key_path = bq_key_path
        self.bq_key = bq_key_name
        self.bq_project = bq_project
        self.bq_credentials = None
        self.bq_client = None

        # SQL Variables
        self.progress_update('Initialising SQL Variables', print_line=False, print_value=False)
        self.sql_key_path = sql_key_path
        self.sql_key = sql_key_name
        self.sql_server = sql_server
        self.sql_connection = None

    def thg_log(self):
        """
        INTERNAL FUNCTION
        """
        if self.temp_set_logging is None or self.temp_set_logging is False:
            print('=' * 99)
            print('=' * 99)
            print("""
    @&&&&&&&&&&&&&&&&&&&&&&&       &&&&&&&%           &&&&&&&.              &&&&&&&&&&&@&&.        
    &&&&&&&&&&&&&&&&&&&&&&&&       &&&&&&&%           &&&&&&&.          @@&&&&&&&&&&&&&&&&&&&&/    
    ,.......&&&&&&&&........       &&&&&&&%           &&&&&&&.        @&&&&&&&&&&/..*&&&&&&&@      
            &&&&&&&@               &&&&&&&%           &&&&&&&.      ,&&&&&&&@             @        
            &&&&&&&@               &&&&&&&%           &&&&&&&.      &&&&&&&&                       
            &&&&&&&@               &&&&&&&&&&&&&&&&&&&&&&&&&&.     .&&&&&&&             ,,,,,,.    
            &&&&&&&@               &&&&&&&&&&&&&&&&&&&&&&&&&&.      &&&&&&&.            &&&&&&*    
            &&&&&&&@               &&&&&&&%           &&&&&&&.      @&&&&&&@/           &&&&&&*    
            &&&&&&&@               &&&&&&&%           &&&&&&&.       &&&&&&&&&@        /@&&&&&*    
            &&&&&&&@               &&&&&&&%           &&&&&&&.         &&&&&&&&&&&&&&&&&&&&&&&*    
            &&&&&&&@               &&&&&&&%           &&&&&&&.            &&&&&&&&&&&&&&&&@&.       
     
    CsPy Uploading Python Package Version: {}""".format(self.version))
            print('=' * 99)

    def insert_line(self):
        """
        INTERNAL FUNCTION
        """
        if self.setting.logging:
            print('=' * 99)

    def log(self, string):
        """
        INTERNAL FUNCTION
        """
        if self.setting.logging:
            print(dt.datetime.now(), ': ', string)

    def progress_update(self, string, print_line, print_value):
        """
        INTERNAL FUNCTION
        """
        self.job_details['Job Progress'] = string
        if self.setting.logging:
            if print_line:
                self.insert_line()
            if print_value:
                print("Job Progress: {}".format(string))

    def get_vm_status(self):
        """
        INTERNAL FUNCTION
        """
        self.job_details['Job Progress'] = 'Getting Run Location'
        self.log("Getting Run Location")
        computer_node = pl.node()
        if left(computer_node, 2) == 'de' or left(computer_node, 2) == 'gb':
            self.vm_status = True
            self.log('Running on VM.')
            file = sys.modules['__main__'].__file__
            directory_name, file_name = os.path.split(os.path.abspath(file))
            self.job_details['Location On VM'] = str(directory_name)
            self.job_details['Script Name'] = file_name

        elif left(computer_node, 5) == 'UK-LT' or left(computer_node, 3) == 'THG' or left(computer_node,
                                                                                          7) == 'DESKTOP':
            self.vm_status = False
            self.log('Running Locally.')

        else:
            self.vm_status = False
            self.log('Running locally.')

    def get_save_file_path(self):
        """
        INTERNAL FUNCTION
        """
        try:
            self.job_details['Job Progress'] = 'Getting Save File Path'
            self.log("Getting Save File Path")
            if self.save_file_path is None:
                self.log("save_file_path Not Provided Creating Temporary Data Folder.")
                file = sys.modules['__main__'].__file__
                directory_name, file_name = os.path.split(os.path.abspath(file))
                directory_name = str(directory_name).replace("\\", "/") + "/"
                folder_path = directory_name + "DATA"
                i = 1
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                else:
                    flag = 0
                    while flag == 0:
                        folder_path = directory_name + "DATA"
                        folder_path = folder_path + "_" + str(i)
                        if not os.path.exists(folder_path):
                            os.mkdir(folder_path)
                            flag = 1
                        else:
                            i += 1
                self.log("Created Temporary DATA Folder: {}".format(folder_path))
                self.save_file_path = folder_path + '/'

            else:
                self.log('Using user defined save path: {}'.format(self.save_file_path))
                self.setting.use_user_defined_save_file_path = True

        except Exception as e:
            self.job_details['Error'] = str(e)
            self.log('Error: {}'.format(e))
            self.run_script_error(error="Failed To Get Save_File_Path",
                                  solution="Check The Script's Logs For Further Detail"
                                  )

        finally:
            self.send_failure_email()

    def get_bq_variables(self):
        """
        INTERNAL FUNCTION
        """
        try:
            if self.bq_key_path is None:
                if self.vm_status and self.use_account:
                    if self.account.info['key_folder_path'] is None:
                        self.bq_key_path = os.getcwd()
                    else:
                        self.bq_key_path = self.account.info['key_folder_path']
                else:
                    self.bq_key_path = os.getcwd()

            if self.bq_project is None:
                if self.use_account:
                    self.bq_project = self.account.info['bq_server']
                else:
                    self.log('Using Default SQL Server Connection: agile-bonbon-662.')
                    self.bq_project = "agile-bonbon-662"

            if self.bq_key is None:
                if self.use_account:
                    self.bq_key = self.account.info['bq_key']
                else:
                    self.bq_key = 'bq_key.json'

            self.job_details['BQ Project'] = self.bq_project

        except Exception as e:
            self.job_details['Error'] = str(e)
            self.log('Error: {}'.format(e))
            self.run_script_error(error="Failed To Get BQ Variables",
                                  solution="Check The Script's Logs For Further Detail"
                                  )

        finally:
            self.send_failure_email()

    def get_sql_variables(self):
        """
        INTERNAL FUNCTION
        """
        try:
            if self.sql_key_path is None:
                if self.vm_status and self.use_account:
                    if self.account.info['key_folder_path'] is None:
                        self.sql_key_path = os.getcwd()
                    else:
                        self.sql_key_path = self.account.info['key_folder_path']
                else:
                    self.sql_key_path = os.getcwd()

            if self.sql_server is None:
                if self.use_account:
                    self.log('Using Account SQL Server Connection: {}'.format(self.account.info['sql_server']))
                    self.sql_server = self.account.info['sql_server']
                else:
                    self.log('Using Default SQL Server Connection: ReportingAdhoc.')
                    self.sql_server = 'ReportingAdhoc'
            else:
                self.log("Using User Input SQL Server Connection: {}".format(self.sql_server))

            if self.sql_key is None:
                if self.use_account:
                    self.sql_key = self.account.info['sql_key']
                else:
                    self.sql_key = 'sql_key.json'

            self.job_details['SQL Server'] = self.sql_server

        except Exception as e:
            self.job_details['Error'] = str(e)
            self.log('Error: {}'.format(e))
            self.run_script_error(error="Failed To Get SQL Variables",
                                  solution="Check The Script's Logs For Further Detail"
                                  )

        finally:
            self.send_failure_email()

    def data_frame_info(self, start, end, df):
        """
        INTERNAL FUNCTION
        """
        try:
            self.log("Data Collected")
            if self.setting.logging:
                print("")
                print("DataFrame Info:")
                print("""   Read from: """, self.input_data_from)
                print("""   Runtime:   """, hf.format_timespan((end - start).total_seconds()))
                print("""   Row Count: """, len(df))
                print("""   Byte Size: """, df.memory_usage(index=True).sum())
                self.job_details['Bytes Uploaded'] = df.memory_usage(index=True).sum()

        except Exception as e:
            self.job_details['Error'] = str(e)
            self.log('Error: {}'.format(e))
            self.run_script_error(error="Failed To Get Data Frame Info",
                                  solution="Check The Script's Logs For Further Detail"
                                  )

        finally:
            self.send_failure_email()

    def get_sql_connection(self):
        """
        INTERNAL FUNCTION
        """
        self.job_details['Job Progress'] = 'Loading SQL Account'
        self.log('Loading SQL Service Account')
        sql_key = os.path.join(self.sql_key_path, self.sql_key)
        try:
            with open(sql_key, 'rb') as file:
                sql_account_data = json.load(file)
                self.log('SQL Service Account Loaded')

        except Exception as e:
            self.log('Failed To Load SQL Service Account')
            self.log('Error: {}'.format(e))
            self.run_script_error(error="Failed To Load SQL Service Account",
                                  solution="Check The Script's Logs For Further Detail"
                                  )

        finally:
            self.send_failure_email()

        self.job_details['Job Progress'] = 'Creating SQL Connection'
        self.log('Creating SQL Connection')
        try:
            self.job_details['SQL Account'] = sql_account_data['username']
            password = sql_account_data['password']
            self.sql_connection = pymssql.connect(server=self.sql_server,
                                                  user=self.job_details['SQL Account'],
                                                  password=password
                                                  )
            self.log('SQL Connection Created')
            if self.setting.logging:
                print("")
                print('SQL Connection Details:')
                print("""   SQL Service Account: {}""".format(self.job_details['SQL Account']))
                print("""   SQL Server:          {}""".format(self.sql_server))
                print("")

        except Exception as e:
            self.log('Failed To Create SQL Connection')
            self.job_details['Error'] = str(e) + '\n Failed To Create SQL Connection'
            self.log('Error: {}'.format(e))
            self.run_script_error(error="Failed To Create SQL Connection",
                                  solution="Check The Script's Logs For Further Detail"
                                  )

        finally:
            self.send_failure_email()

    def get_bq_connection(self):
        """
        INTERNAL FUNCTION
        """
        try:
            self.job_details['Job Progress'] = 'Loading BQ Service Account'
            self.log('Loading BQ Service Account')
            scopes = ['https://www.googleapis.com/auth/bigquery', 'https://www.googleapis.com/auth/drive.readonly']
            bq_key = os.path.join(self.bq_key_path, self.bq_key)

            self.bq_credentials = service_account.Credentials.from_service_account_file(bq_key, scopes=scopes)
            self.bq_client = Client(project=self.bq_project, credentials=self.bq_credentials)
            with open(bq_key, 'r') as key_file:
                text = key_file.read()
                key_info = eval(text)
                self.job_details['BQ Account Used'] = key_info['client_email']
            self.log('BQ Connection Created')
            if self.setting.logging:
                print("")
                print('BQ Connection Details:')
                print("""   BQ Service Account: {}""".format(self.job_details['BQ Account Used']))
                print("""   BQ Server: {}""".format(self.bq_project))

        except Exception as e:
            self.log('Error: {}'.format(e))
            self.job_details['Error'] = str(e) + '\n Failed To Create BQ Connection'
            self.run_script_error(error="Failed To Get Input Data Type",
                                  solution="Check The Script's Logs For Further Detail"
                                  )

        finally:
            self.send_failure_email()

    def query_classification(self):
        """
        INTERNAL FUNCTION
        """
        try:
            if self.query is not None and self.input_data_from is None:
                self.job_details['Job Progress'] = 'Classifying Query'
                self.log('Classifying Query')
                sql_flags = ['set ansi_nulls off', 'set nocount on', 'set ansi_warnings off', 'datawarehouse',
                             'if object_id', 'declare', '(nolock)', 'marketing.cos', '.dbo.', '.thg.', 'nero',
                             'brand_reporting']
                bq_flags = ['from `', 'with', 'ditto', 'lower', '_table_suffix', 'eu_data', '1,2', '0_larry_tt',
                            '0_']
                sql_count = 0
                bq_count = 0
                for i in sql_flags:
                    if i in self.query.lower():
                        sql_count += 1
                for i in bq_flags:
                    if i in self.query.lower():
                        bq_count += 1

                if sql_count > bq_count:
                    self.input_data_from = 'SQL'
                    self.job_details['SQL Access'] = 'Yes'
                    self.job_details['BQ Access'] = 'Write'

                elif sql_count < bq_count:
                    self.input_data_from = 'BQ'
                    self.job_details['SQL Access'] = 'No'
                    self.job_details['SQL Access'] = 'Read & Write'

                elif sql_count == bq_count:
                    self.log('Could Not Classify Query')
                    self.job_details['Error'] = 'Could not classify Query.'

            else:
                pass

        except Exception as e:
            self.job_details['Error'] = str(e)
            self.log('Error: {}'.format(e))
            self.run_script_error(error="Failed To Classify Query",
                                  solution="Check The Script's Logs For Further Detail"
                                  )

        finally:
            self.send_failure_email()

    def delete_folder_contents(self, data_type):
        """
        INTERNAL FUNCTION
        """
        if self.setting.logging:
            print("")
        self.log("Deleting {0} Files From: {1}".format(data_type, self.save_file_path))
        file_type_check = None
        file_type_check_length = None

        if data_type == 'CSV':
            file_type_check = 'csv'
            file_type_check_length = 3
        elif data_type == 'JSON':
            file_type_check = 'json'
            file_type_check_length = 4

        for file in os.listdir(self.save_file_path):
            if right(file, file_type_check_length) == file_type_check:
                self.log("Deleting: {}".format(file))
                os.unlink(self.save_file_path + file)

    def send_failure_email(self):
        """
        INTERNAL FUNCTION
        """
        if self.run_error:
            if not self.setting.testing and self.vm_status and self.use_account:
                sender = self.account.info['data_team_vm_email']
                receiver = '{0}; {1}'.format(
                    self.account.info['data_team_email'],
                    self.account.info['email']
                )

                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = receiver
                msg['Subject'] = 'VM Script: {} Failed to Run.'.format(self.job_details['Script Name'])

                message = """
                <p><strong>Time Ran:</strong> {0} <br>
                <strong>Script Owner:</strong> {1} <br><br>
                <strong>The Script located at:</strong> {2}\\{3} <br>
                <strong>The Script failed at:</strong> {4} - {5} <br><br>
                <strong>Error Message:</strong> {6} <br>
                <strong>Error Solution:</strong> {7} <br><br>
                For Further Details Please Read The Script Logs On The VM <br>
                <strong>CsPy Version: {8}</p>
                """.format(self.job_details['Run Date'],
                           self.account.info['first_name'] + ' ' + self.account.info['surname'],
                           self.job_details['Location On VM'],
                           self.job_details['Script Name'],
                           self.job_details['Job Portion'],
                           self.job_details['Job Progress'],
                           self.job_details['Error Message'],
                           self.job_details['Solution'],
                           self.version
                           )

                msg.attach(MIMEText(message, 'HTML'))

                with SMTP(host="fortimail.gslb.thehut.local", port=25) as smtp:
                    try:
                        smtp.sendmail(sender, receiver, msg.as_string())
                        self.log('Failed Script Email sent.')
                    except SMTPException as error:
                        self.log('Failed Script Email not sent Error: {0}.'.format(error))

            else:
                self.log("Failed Email Alert Not Sent. Only Available On The VM Whilst Using Accounts")

            self.exit()

    def run_script_error(self, error=None, solution=None):
        """
        INTERNAL FUNCTION
        """
        time.sleep(2)
        self.run_error = True
        self.job_details['Error Message'] = error
        self.job_details['Solution'] = solution
        raise GeneralScriptError(
            job_progress=self.job_details['Job Progress'],
            message=self.job_details['Error Message'],
            solution=self.job_details['Solution']
        )

    def exit(self):
        """
        INTERNAL FUNCTION
        """
        if self.run_error:
            self.run_error = False
            self.sys_exit = True
            sys.exit(1)


class JobSettings:
    """
    Desc:
        JobSettings (class): Supporting class for BaseJob to create a set of settings under a single reference

    Args:
        logging (bool): Used to toggle logging in BaseJob functions
        testing (bool): User to toggle Failure Emails in BaseJob functions

    Returns:
        No values are returned

    Raises:
        No exceptions raise in this initialisation class
    """

    def __init__(self, logging=None, testing=None):
        self.logging = logging
        if self.logging is None:
            self.logging = True
        else:
            self.logging = logging

        self.testing = testing
        if self.testing is None:
            self.testing = False
        else:
            self.testing = testing

        self.job_type = None
        self.date_conversion = False
        self.clear_data_cache = True
        self.use_user_defined_save_file_path = False
        self.open_file = False

    def insert_line(self):
        """
        INTERNAL FUNCTION
        """
        if self.logging:
            print(
                '=' * 99)

    def log(self, string):
        """
        INTERNAL FUNCTION
        """
        if self.logging:
            print(dt.datetime.now(), ': ', string)

    def log_settings(self):
        """
        INTERNAL FUNCTION
        """
        if self.logging and self.job_type == 'Upload':
            print("")
            print('Upload Settings:')
            print("""   Logging: {}""".format(self.logging))
            print("""   Clear Data cache: {}""".format(self.clear_data_cache))
            print("""   Date Conversion: {}""".format(self.date_conversion))
            print("""   Testing: {}""".format(self.testing))

        elif self.logging and self.job_type == 'Download':
            print("")
            print('Download Settings:')
            print("""   Clear Data Save Location: {}""".format(self.clear_data_cache))
            print("""   Open File: {}""".format(self.open_file))
            print("""   Testing: {}""".format(self.testing))

        else:
            print('Logging turned off.')

    def update(self, job_type, clear_data_cache, date_conversion, open_file):
        """
        INTERNAL FUNCTION
        """
        self.log("Setting Upload Job Settings")
        if job_type == 'Upload':
            self.job_type = job_type

            if clear_data_cache is not None:
                self.clear_data_cache = clear_data_cache

            if date_conversion is not None:
                self.date_conversion = date_conversion

        elif job_type == 'Download':
            self.job_type = job_type

            if clear_data_cache is not None:
                self.clear_data_cache = clear_data_cache

            if open_file is not None:
                self.open_file = open_file

        self.log_settings()


class UploadJob(BaseJob):
    """
    Desc:
        UploadJob (class): Class used to initialise an upload job and run the upload to Big Query
                    Notes: This will upload data from various inputs into BQ. Mainly used for data pipelines

    Args:
        query (str): If uploading via SQL or BQ this is the query you wish to run
              Notes: Not needed if you are uploading via a CSV, JSON or DATAFRAME data types

        data_file (str): IF uploading via CSV or JSON this is the full file path to the data file you wish to upload
                  Notes: Not needed if you are uploading via a SQL, BQ or DATAFRAME data types

        dataframe (dataframe): If uploading via DATAFRAME this is the pandas dataframe data you wish to upload
                        Notes: Not needed if you are uploading via a SQL, BQ, CSV or JSON data types

        bq_project (str): The name of the big query project you wish to upload to

        bq_dataset (str): The name of the big query dataset you wish to upload to

        bq_table (str): The name of the big query table you wish to upload
                 Notes: If date partitioning add a "_" to the end to gain additional functionality in the BQ UI

        bq_key_path (str): The file path to the folder that your BQ service account is stored
                  Example: "C:/Users/RobinsonJa/Service_Accounts/"

        bq_key_name (str): Name of your BQ service account file
                  Example: "bq_key.json"

        sql_server (str): The connection name of the sql server you wish to read data from
                   Notes: Not needed if you are uploading via BQ, CSV, JSON or DATAFRAME
                   Notes: Not needed if you are using an account and plan on using your default server

        sql_key_path (str): The file path to the folder that your SQL service account is stored
                   Example: "C:/Users/RobinsonJa/Service_Accounts/"
                     Notes: Not needed if you are uploading via BQ, CSV, JSON or DATAFRAME

        sql_key_name (str): Name of your SQL service account file
                   Example: "sql_key.json"
                     Notes: Not needed if you are uploading via BQ, CSV, JSON or DATAFRAME
                     Notes: Not needed if you are using an account and plan on using your default key name

    Optional Args:
        input_data_from (str): Type of data that will be used in the job.
                        Notes: Accepted inputs are SQL, BQ, CSV, JSON, DATAFRAME
                        Notes: Optional but recommended argument

        schema (list): The schema of your data to be upload to BQ. In the format of a list consisting of tuples
              Example: [("order_timestamp", "TIMESTAMP"),("review_comments", "STRING")]
                Notes: If not supplied job will upload using googles schema AutoDetect feature
                Notes: Optional but recommended argument

        columns (list): A list of columns names used to replace the column names collected in data collection
              Examples: ["column_1", "column_2"]
                 Notes: Spaces or special characters in the column names are not accepted by the BQ API

        date_column (str): If you wish to date partition this is the column name the data with be partitioned by
                    Notes: Column can be either a YYYY-MM-DD format or a YYYYMMDD format
                    Notes: Required if you are date paritioning your data

        upload_data_type (str): The method by which you wish your data to be upload to BQ.
                         Notes: Accepted inputs are CSV, JSON, DATAFRAME. Defaults to CSV if not inputted

        bq_upload_type (str): The BQ job configuration type of upload
                       Notes: Accepted inputs are Truncate, Append, Empty. Defaults to Truncate if not inputted

        save_file_path (str): The file path used to store data files for Upload or Download
                     Example: "C:/Users/RobinsonJa/data/"
                       Notes: If not supplied job will create a temporary DATA folder then is remove after upload
                       Notes: Optional but recommended argument

        account_first_name (str): First name used on the account you wish to use
                           Notes: Used to read the account details for the given first name
                           Notes: Using accounts will require less overall inputs per job

        account_surname (str): Surname used on the account you wish to use
                           Notes: Used to read the account details for the given first name
                           Notes: Using accounts will require less overall inputs per job

        account_file_path (str): The file path to the folder that your account is stored
                        Example: "C:/Users/RobinsonJa/account/"
                          Notes: Not needed if your account file is within the working directory of your script
                          Notes: Not needed on the VM if you have saved the account in the designated folder

    Setting Args:
        set_logging (bool): Set True for console output. Set False for no console output
                     Notes: Defaults to True

        set_clear_data_cache (bool): Set True to delete any temporary files created. Set False to keep temporary files
                              Notes: Defaults to True

        set_testing (bool): Set True when testing on the VM to stop audit logs being uploaded and failure emails
                     Notes: Defaults to False

        set_date_conversion (bool): Set True to convert any DATE or DATETIME columns to date keys with data type INTEGER
                             Notes: Must supply schema to state which columns are either DATE or DATETIME types
                             Notes: Defaults to False

    Returns:
        No values are returned as this class just initialises a Job

    Raises:
        InputError: When an input is supplied incorrectly
        ColumnMissingError: When a column is not present in the dataset but is within the schema
    """

    def __init__(self, query=None, input_data_from=None, data_file=None, dataframe=None,
                 schema=None, columns=None, date_column=None, upload_data_type=None,
                 bq_project=None, bq_dataset=None, bq_table=None, bq_key_path=None, bq_key_name=None,
                 bq_upload_type=None,
                 sql_server=None, sql_key_path=None, sql_key_name=None, save_file_path=None,
                 account_first_name=None, account_surname=None, account_file_path=None,
                 set_logging=None, set_clear_data_cache=None, set_testing=None, set_date_conversion=None,
                 ):
        super().__init__(query, input_data_from,
                         bq_project, bq_key_path, bq_key_name,
                         sql_server, sql_key_path, sql_key_name, save_file_path,
                         account_first_name, account_surname, account_file_path,
                         set_logging, set_testing)

        # Initialising Upload Job
        self.job_details['Job Portion'] = 'Initialising Upload Job'
        self.progress_update('Initialising Upload Job', print_line=True, print_value=True)
        self.job_type = 'Upload'
        self.setting.update(self.job_type, set_clear_data_cache, set_date_conversion, None)
        self.bq_project = bq_project
        self.bq_dataset = bq_dataset
        self.bq_table = bq_table

        # Determine Input Data Type
        self.progress_update('Searching For Input Data Type', print_line=True, print_value=True)
        self.data_file = data_file
        self.dataframe = dataframe
        self.get_input_data_type()

        # BQ Variables
        self.progress_update('Creating Big Query Connection', print_line=True, print_value=True)
        self.get_bq_variables()
        self.get_bq_connection()

        # Load Data Into DataFrame
        self.progress_update('Getting Data From {}'.format(self.input_data_from), print_line=True, print_value=True)
        self.job_details['Upload Type'] = 'From ' + self.input_data_from
        self.columns = columns
        self.data = self.load_data()

        # Cleaning DataFrame
        self.progress_update('Cleaning DataFrame', print_line=True, print_value=True)
        self.schema = schema
        self.schema_columns = None
        self.get_schema()
        self.int_convert()
        self.date_convert()

        # Build DF into upload file type CSV/Json/DF
        self.progress_update('Preparing Upload', print_line=True, print_value=True)
        self.save_path = None
        self.date_column = date_column
        self.upload_dataframe = {}
        self.upload_data_type = upload_data_type

        # Build BQ Job Config
        self.job_details['Job Progress'] = 'Creating Big Query Job Config'
        self.log("Creating Big Query Job Config")
        self.bq_upload_type = bq_upload_type
        self.dataset_ref = DatasetReference(project=self.bq_project, dataset_id=self.bq_dataset)
        self.job_details['BQ Dataset'] = self.bq_dataset
        self.job_details['BQ Table'] = self.bq_table
        self.job_config = LoadJobConfig()
        self.create_job_config()

    def get_input_data_type(self):
        """
        INTERNAL FUNCTION
        """
        try:
            self.log('Searching For Input Data Type')
            if self.input_data_from is None:
                self.log('input_data_from Not Provided Reading Inputs To Diagnose Input Data Type')
                count = 0
                for i in (self.query, self.data_file, self.dataframe):
                    if i is not None:
                        count += 1

                if count != 1:
                    if count > 1:
                        self.run_error = True
                        self.job_details['Error Message'] = "Too Many Data Inputs Used"
                        self.job_details['Solution'] = "Only One Of These Arguments Can Be Used: query, data_file or " \
                                                       "dataframe "
                        raise InputError(job_progress=self.job_details['Job Progress'],
                                         input_variable_name="Input Data",
                                         message=self.job_details['Error Message'],
                                         solution=self.job_details['Solution']
                                         )

                    elif count == 0:
                        self.run_error = True
                        self.job_details['Error Message'] = "Not Enough Variables Assigned To Classify Input Data Type"
                        self.job_details['Solution'] = "Use input_data_from To Explicitly State Data To Be Uploaded"
                        raise InputError(job_progress=self.job_details['Job Progress'],
                                         input_variable_name="Input Data",
                                         message=self.job_details['Error Message'],
                                         solution=self.job_details['Solution']
                                         )
                    pass

                else:
                    if self.query is not None:
                        self.query_classification()
                    elif self.data_file is not None:
                        if right(self.data_file, 3).lower() == 'csv':
                            self.input_data_from = 'CSV'
                        elif right(self.data_file, 4).lower() == 'json':
                            self.input_data_from = 'JSON'
                    elif self.dataframe is not None:
                        self.input_data_from = 'DATAFRAME'

                    self.log('Input Data Type Found: {}'.format(self.input_data_from))

            else:
                if self.input_data_from in ('SQL', 'BQ', 'CSV', 'JSON', 'DATAFRAME'):
                    self.log('User Defined Input Data Type Found: {}'.format(self.input_data_from))
                else:
                    self.run_error = True
                    self.job_details['Error Message'] = "Variable input_data_from Value \"{}\" Not Recognised".format(
                        self.input_data_from)
                    self.job_details['Solution'] = "Accepted input_data_from Values Are: SQL, BQ, CSV, JSON, DATAFRAME"
                    raise InputError(job_progress=self.job_details['Job Progress'],
                                     input_variable_name="input_data_from",
                                     message=self.job_details['Error Message'],
                                     solution=self.job_details['Solution']
                                     )

            if self.input_data_from == 'BQ':
                self.job_details['BQ Access'] = 'Read & Write'

        except Exception as e:
            if self.sys_exit:
                pass
            else:
                self.job_details['Error'] = str(e)
                self.log('Error: {}'.format(e))
                self.run_script_error(error="Failed To Get Input Data Type",
                                      solution="Check The Script's Logs For Further Detail"
                                      )

        finally:
            self.send_failure_email()

    def load_data(self):
        """
        INTERNAL FUNCTION
        """
        try:
            start_time = dt.datetime.now()
            df = pd.DataFrame()
            if self.input_data_from == 'SQL':
                self.log("Getting SQL Credentials")
                self.get_sql_variables()
                self.log('Reading From SQL Server: {}'.format(self.sql_server))
                self.query = """
                set ansi_nulls off 
                set nocount on 
                set ansi_warnings off
                """ + self.query
                self.get_sql_connection()
                self.log('Collecting Data...')
                df = pd.read_sql(sql=self.query, con=self.sql_connection)

            elif self.input_data_from == 'BQ':
                self.log('Reading From BQ Server: {}'.format(self.bq_project))
                self.log('Collecting Data...')
                df = pd.read_gbq(query=self.query, project_id=self.bq_project, dialect='standard',
                                 credentials=self.bq_credentials)

            elif self.input_data_from == 'CSV':
                self.log('Reading From CSV File: {}'.format(self.data_file))
                self.log('Collecting Data...')
                df = pd.read_csv(self.data_file, header=0)

            elif self.input_data_from == 'JSON':
                self.log('Reading From JSON File: {}'.format(self.data_file))
                self.log('Collecting Data...')
                df = pd.read_json(self.data_file)

            elif self.input_data_from == 'DATAFRAME':
                self.log("Reading From User Input Dataframe")
                self.log("Collecting Data...")
                df = self.dataframe

            end_time = dt.datetime.now()
            if self.columns is not None:
                self.log("Using User Defined Column Names")
                df.rename(columns=self.columns)
                self.log("Column Names Updated")

            self.data_frame_info(start_time, end_time, df)
            return df

        except Exception as e:
            if self.sys_exit:
                pass
            else:
                self.job_details['Error'] = str(e)
                self.log('Error: {}'.format(e))
                self.run_script_error(error="Failed To Load Data",
                                      solution="Check The Script's Logs For Further Detail"
                                      )

        finally:
            self.send_failure_email()

    def get_schema(self):
        """
         INTERNAL FUNCTION
         """
        if self.schema is not None:
            self.job_details['Job Progress'] = 'Getting User Defined Schema'
            self.schema_columns = []
            temp_schema = []
            try:
                for i in self.schema:
                    name = i[0]
                    field_type = i[1]
                    temp_schema.append(sf(name=name, field_type=field_type, mode="NULLABLE"))
                    self.schema_columns.append(name)
                self.schema = temp_schema

            except Exception as e:
                self.log('Error: {}'.format(e))
                self.job_details['Error'] = e
                self.run_error = True
                self.job_details['Error Message'] = "Could Not Read Schema"
                self.job_details['Solution'] = "Check Over Schema Variable. Code Documentation Has Schema Format"

                raise InputError(job_progress=self.job_details['Job Progress'],
                                 input_variable_name="schema",
                                 message=self.job_details['Error Message'],
                                 solution=self.job_details['Solution']
                                 )

            finally:
                self.send_failure_email()

        try:
            if len(self.data.columns) != len(self.schema_columns):
                self.job_details['Error Message'] = "Schema Mismatch: {} Data Columns. But {} Schema Columns".format(
                    len(self.data.columns), len(self.schema_columns))
                self.job_details['Solution'] = "Check Over Schema Variable And Dataset To Align Column Names"

                raise InputError(job_progress=self.job_details['Job Progress'],
                                 input_variable_name="schema",
                                 message=self.job_details['Error Message'],
                                 solution=self.job_details['Solution']
                                 )
            else:
                num = 0
                column_checker = []
                for i in self.data.columns:
                    column_name = (i, self.schema_columns[num], num)
                    column_checker.append(column_name)
                    num += 1

                for i in column_checker:
                    if i[0] != i[1]:
                        message = "Mismatched Columns Names In Column Number {0}".format(i[2]) + \
                                "Data Column Name \"{0}\" Does Not Match Schema Column Name \"{1}\"".format(i[0], i[1]),
                        self.job_details['Error Message'] = message
                        self.job_details['Solution'] = "Check Over Schema Variable And Dataset To Align Column Names"
                        raise InputError(job_progress=self.job_details['Job Progress'],
                                         input_variable_name="schema",
                                         message=self.job_details['Error Message'],
                                         solution=self.job_details['Solution']
                                         )
                    else:
                        pass

        except Exception as e:
            self.job_details['Error'] = str(e)
            self.log('Error: {}'.format(e))
            self.run_script_error(error="Failed To Classify Query",
                                  solution="Check The Script's Logs For Further Detail"
                                  )

        finally:
            self.send_failure_email()

    def int_convert(self):
        """
        INTERNAL FUNCTION
        """
        try:
            if self.schema is not None:
                self.job_details['Job Progress'] = 'Cleaning Integer Columns For Upload.'
                self.log("Cleaning Integer Columns For Upload")
                convert_columns = []
                new_df = self.data
                for i in self.schema:
                    if i.field_type == 'INTEGER':
                        convert_columns.append(i.name)

                if len(convert_columns) != 0:
                    for i in convert_columns:
                        try:
                            if i not in new_df.columns:
                                self.job_details['Error Message'] = "Could Not Find Column {} For Conversion".format(i)
                                self.job_details['Solution'] = "Check Over Schema And Dataset To Align Column Names"

                                raise ColumnMissingError(
                                    missing_column=i,
                                    job_progress=self.job_details['Job Progress']
                                )

                            new_df[i] = new_df[i].astype('float')
                            new_df[i] = new_df[i].astype('Int64')

                        except Exception as e:
                            convert_columns.remove(i)
                            self.log('Failed To Convert Column: {} To INT'.format(i))
                            self.log('Error: {}'.format(e))

                self.data = new_df

            else:
                self.log("Integer Cleaning Can Not Run As Schema Is Set To Auto Detect")

        except Exception as e:
            self.job_details['Error'] = str(e)
            self.log('Error: {}'.format(e))
            self.run_script_error(error="Failed To Complete Integer Conversion Whilst Cleaning Dataset",
                                  solution="Check The Script's Logs For Further Detail"
                                  )

        finally:
            self.send_failure_email()

    def date_convert(self):
        """
        INTERNAL FUNCTION
        """
        try:
            if self.setting.date_conversion and self.schema is not None:
                self.job_details['Job Progress'] = 'Converting Date Columns To Date Keys.'
                self.log("Converting Date Columns To Date Keys")
                convert_columns = []
                new_schema = []
                new_df = self.data
                for i in self.schema:
                    if i.field_type in ('DATETIME', 'DATE'):
                        convert_columns.append(i.name)

                if len(convert_columns) != 0:
                    self.log('Date Columns To Be Converted To Keys: {}'.format(str(convert_columns)))

                    for i in convert_columns:
                        try:
                            self.log('Converting date column {}'.format(i))
                            if i not in new_df.columns:
                                self.job_details['Error Message'] = "Could Not Find Column {} For Conversion".format(i)
                                self.job_details['Solution'] = "Check Over Schema And Dataset To Align Column Names"

                                raise ColumnMissingError(
                                    missing_column=i,
                                    job_progress=self.job_details['Job Progress']
                                )
                            new_df[i] = pd.to_datetime(new_df[i])
                            new_df[i] = new_df[i].fillna(dt.datetime(1990, 9, 14))
                            new_df[i] = new_df[i].dt.strftime('%Y%m%d').astype(int)
                            new_df[i] = new_df[i].replace(19900914, np.nan)

                        except Exception as e:
                            convert_columns.remove(i)
                            self.log('Failed to convert {} column to a date.'.format(i))
                            self.log('Error: {}'.format(e))

                    for i in self.schema:
                        if i.name in convert_columns:
                            x = sf(name=i.name, field_type='INTEGER', mode=i.mode)
                            new_schema.append(x)
                        else:
                            new_schema.append(i)

                    self.schema = new_schema
                    self.log('Updated Schema To Reflect Converted Columns')
                    self.log("Date Columns Converted: {}".format(convert_columns))
                    self.data = new_df

                else:
                    self.log("Date Conversion Skipped As No Date Columns Found")

            else:
                self.log("Date Conversion Skipped As Date Conversion Setting = False")

        except Exception as e:
            self.job_details['Error'] = str(e)
            self.log('Error: {}'.format(e))
            self.run_script_error(error="Failed To Complete Date Conversion Whilst Cleaning Dataset",
                                  solution="Check The Script's Logs For Further Detail"
                                  )

        finally:
            self.send_failure_email()

    def create_job_config(self):
        """
        INTERNAL FUNCTION
        """
        try:
            self.log("Creating Big Query Upload Job Configuration.")
            if self.bq_upload_type is not None and self.bq_upload_type not in ('Truncate', 'Append', 'Empty'):
                self.job_details['Error Message'] = "Variable input_data_from Value \"{}\" Not Recognised".format(
                    self.bq_upload_type)
                self.job_details['Solution'] = "Accepted bq_upload_type Values Are: Truncate, Append, Empty"

                raise InputError(job_progress=self.job_details['Job Progress'],
                                 input_variable_name="bq_upload_type",
                                 message=self.job_details['Error Message'],
                                 solution=self.job_details['Solution']
                                 )

            if self.bq_upload_type == 'Truncate':
                self.job_config.write_disposition = 'WRITE_TRUNCATE'
                self.log("BQ Upload Type Set To Write Truncate")

            elif self.bq_upload_type == 'Append':
                self.job_config.write_disposition = 'WRITE_APPEND'
                self.log("BQ Upload Type Set To Write Append")

            elif self.bq_upload_type == 'Empty':
                self.job_config.write_disposition = 'WRITE_EMPTY'
                self.log("BQ Upload Type Set To Write Empty")

            else:
                self.job_config.write_disposition = 'WRITE_TRUNCATE'
                self.log("BQ Upload Type Set To Default Value Of Write Truncate")

            self.job_config.skip_leading_rows = 1
            self.job_config.source_format = self.upload_data_type

            if self.schema is not None:
                self.log("User Defined Schema Detected.")
                self.job_config.schema = self.schema

            else:
                self.log("Schema Not Detected Using Autodetect Schema.")
                self.job_config.autodetect = True
                self.setting.date_conversion = False

        except Exception as e:
            self.job_details['Error'] = str(e)
            self.log('Error: {}'.format(e))
            self.run_script_error(error="Failed To Create Big Query Job Config",
                                  solution="Check The Script's Logs For Further Detail"
                                  )

        finally:
            self.send_failure_email()

    def run(self):
        """
        Desc:
            run (function): Run the upload process for a UploadJob

        Args:
            self: All variables built within the UploadJob class

        Returns:
            No values are returned as this function performs an action to upload data

        Raises:
            No exceptions raised in this function
        """
        try:
            self.job_details['Job Portion'] = 'Running Upload Job'
            self.job_details['Job Status'] = 'Ran Successfully'
            self.job_details['Error'] = ''
            self.run_error = False
            self.sys_exit = False

            self.progress_update('Creating Upload Files', print_line=True, print_value=True)
            self.create_upload_files()
            self.progress_update('Uploading to Big query', print_line=True, print_value=True)
            if self.upload_data_type in ('CSV', 'JSON'):
                self.log("Uploading Data As {}".format(self.upload_data_type))
                save_file_type = self.upload_data_type.lower()
                save_file_type_length = len(self.upload_data_type)
                save_path = None
                table_ref = None
                day = None

                for file in os.listdir(self.save_file_path):
                    if right(file, save_file_type_length) == save_file_type:

                        if self.date_column is not None:
                            if left(right(file, save_file_type_length + 6), 5) != '_full':
                                day = left(right(file, save_file_type_length + 9), 8)
                                table_ref = self.dataset_ref.table(self.bq_table + day)
                                save_path = self.save_file_path + file

                        elif self.date_column is None:
                            if left(right(file, save_file_type_length + 6), 5) == '_full':
                                day = ''
                                table_ref = self.dataset_ref.table(self.bq_table)
                                save_path = self.save_file_path + file

                    if save_path is not None:
                        if self.setting.logging:
                            print("")
                        with open(save_path, 'rb') as upload_file:
                            try:
                                self.log("Uploading {0} to {1}".format(self.bq_table + day, self.bq_dataset))
                                upload_job = self.bq_client.load_table_from_file(
                                    file_obj=upload_file, destination=table_ref, job_config=self.job_config)
                                upload_job.result()
                                self.log("Upload Status: {}".format(upload_job.state))

                            except Exception as e:
                                self.log(
                                    "Table {0}{1} failed to upload to {2}".format(self.bq_table, day, self.bq_dataset))
                                self.log("Error: {}".format(e))
                                self.job_details["Error"] = str(e)
                                self.job_details['Job Status'] = 'Ran Successfully'
                                if "400" in str(e):
                                    self.log("Error: {}".format(upload_job.errors[0]['message']))
                                    self.log("Error: {}".format(upload_job.errors[1]['message']))
                                    self.job_details["GA Error"] = "Error: {}".format(upload_job.errors[1]['message'])

                    save_path = None
                    table_ref = None
                    day = None

            if self.upload_data_type == 'DATAFRAME':
                self.job_config.source_format = 'CSV'
                self.log("Uploading Data As DATAFRAME")
                if self.date_column is None:
                    try:
                        if self.setting.logging:
                            print("")
                        self.log("Uploading {0} to {1}".format(self.bq_table, self.bq_dataset))
                        table_ref = self.dataset_ref.table(self.bq_table)
                        upload_job = self.bq_client.load_table_from_dataframe(
                            dataframe=self.data, destination=table_ref, job_config=self.job_config)
                        upload_job.result()
                        self.log("Upload Status: {}".format(upload_job.state))

                    except Exception as e:
                        self.log("Table {0} failed to upload to {1}".format(self.bq_table, self.bq_dataset))
                        self.log("Error: {}".format(e))
                        self.job_details["Error"] = str(e)
                        self.job_details['Job Status'] = 'Ran Unsuccessfully'
                        if "400" in str(e):
                            self.log("Error: {}".format(upload_job.errors[0]['message']))
                            self.log("Error: {}".format(upload_job.errors[1]['message']))
                            self.job_details["GA Error"] = "Error: {}".format(upload_job.errors[1]['message'])

                else:
                    for day, dataframe in self.upload_dataframe.items():
                        try:
                            if self.setting.logging:
                                print("")
                            self.job_details['Table Partitions'] += 1
                            table_ref = self.dataset_ref.table(self.bq_table + day)
                            self.log("Uploading {0} to {1}".format(self.bq_table + day, self.bq_dataset))
                            upload_job = self.bq_client.load_table_from_dataframe(
                                dataframe=dataframe, destination=table_ref, job_config=self.job_config)
                            upload_job.result()
                            self.log("Upload Status: {}".format(upload_job.state))

                        except Exception as e:
                            self.log("Table {0}{1} failed to upload to {2}".format(self.bq_table, day, self.bq_dataset))
                            self.log("Error: {}".format(e))
                            self.job_details["Error"] = str(e)
                            self.job_details['Job Status'] = 'Ran Unsuccessfully'
                            if "400" in str(e):
                                self.log("Error: {}".format(upload_job.errors[0]['message']))
                                self.log("Error: {}".format(upload_job.errors[1]['message']))
                                self.job_details["GA Error"] = "Error: {}".format(upload_job.errors[1]['message'])

        except Exception as e:
            self.log("Error: {}".format(e))
            self.job_details["Error"] = str(e)
            self.job_details['Job Status'] = 'Ran Unsuccessfully'

        finally:
            if self.use_account:
                self.job_details['Owner'] = self.account.info['first_name'] + ' ' + self.account.info['surname']
            else:
                self.job_details['Owner'] = 'Not Defined'

            self.job_details['Runtime'] = (dt.datetime.now() - self.start_time).total_seconds()

            if self.job_details['Error'] != '':
                self.send_email()

            if self.vm_status:
                self.log('Logging Upload to BQ')
                self.run_upload_details()
                self.log('DONE')

            if self.setting.clear_data_cache:
                self.progress_update('Clear Data Cache Set To True. Deleting Temporary Files Created', print_line=True,
                                     print_value=True)
                if self.setting.use_user_defined_save_file_path:
                    self.log('Removing Files From User Defined Data Cache: {}'.format(self.save_file_path))
                    self.delete_folder_contents(data_type=self.upload_data_type)
                else:
                    self.log('Removing Files From Temporary Data cache: {}'.format(self.save_file_path))
                    self.delete_folder_contents(data_type=self.upload_data_type)
                    self.log('Removing Temporary Data cache: {}'.format(self.save_file_path))
                    os.rmdir(self.save_file_path)

    def create_upload_files(self):
        """
        INTERNAL FUNCTION
        """
        if self.upload_data_type is None:
            self.log("Using Default Upload Data Type Of CSV")
            self.upload_data_type = 'CSV'

        elif self.upload_data_type is not None:
            if self.upload_data_type not in ('CSV', 'JSON', 'DATAFRAME'):
                raise InputError(job_progress=self.job_details['Job Progress'],
                                 input_variable_name="upload_data_type",
                                 message="User Defined upload_data_type Value \"{}\" Not Recognised".format(
                                     self.upload_data_type),
                                 solution="Accepted upload_data_type Values Are: CSV, JSON, DATAFRAME"
                                 )

        if self.upload_data_type in ('CSV', 'JSON'):
            self.delete_folder_contents(self.upload_data_type)

        if self.upload_data_type == 'CSV':
            self.save_path = self.save_file_path + "/{}.csv"
            self.data.to_csv(self.save_path.format(self.bq_table + '_full'), index=False, header=True)
            self.job_details['Table Partitions'] = 0

        elif self.upload_data_type == 'JSON':
            self.save_path = self.save_file_path + "/{}.json"
            self.data.to_json(self.save_path.format(self.bq_table + '_full'))
            self.job_details['Table Partitions'] = 0

        if self.date_column is not None:
            self.job_details['Date Partitioned'] = 'Yes'
            if self.date_column not in self.data.columns:
                raise ColumnMissingError(self.date_column, self.job_details['Job Progress'])
                pass

            for day, day_data in self.data.groupby(self.date_column):
                if self.setting.logging:
                    print("")
                self.job_details['Table Partitions'] += 1
                try:
                    daykey = str(day).replace('-', '')
                    day_new = daykey[:8]
                    self.log("Converted Date: {0} To Datekey {1}".format(day, day_new))
                except Exception as e:
                    self.log('Failed to convert {0} to format YYYYMMDD'.format(day))
                    day_new = day
                    self.log('Error: {}'.format(e))

                if self.upload_data_type == 'CSV':
                    self.log("Saving Date Partition CSV For Date: {}".format(day))
                    day_data.to_csv(self.save_path.format(self.bq_table + day_new), index=False, header=True)

                if self.upload_data_type == 'JSON':
                    self.log("Saving Date Partition JSON For Date: {}".format(day))
                    day_data.to_json(self.save_path.format(self.bq_table + day_new))

                if self.upload_data_type == 'DATAFRAME':
                    self.log("Saving Date Partition DATAFRAME For Date: {}".format(day))
                    self.upload_dataframe[day_new] = day_data
                    self.job_details['Table Partitions'] = 0

    def run_upload_details(self):
        """
        INTERNAL FUNCTION
        """
        upload_job_details_schema = [
            sf(name="BQ_Project", field_type="STRING", mode="NULLABLE"),
            sf(name="BQ_Dataset", field_type="STRING", mode="NULLABLE"),
            sf(name="BQ_Table", field_type="STRING", mode="NULLABLE"),
            sf(name="Upload_Type", field_type="STRING", mode="NULLABLE"),
            sf(name="Job_Status", field_type="STRING", mode="NULLABLE"),
            sf(name="Owner", field_type="STRING", mode="NULLABLE"),
            sf(name="Run_Date", field_type="DATETIME", mode="NULLABLE"),
            sf(name="Location_On_VM", field_type="STRING", mode="NULLABLE"),
            sf(name="Script_Name", field_type="STRING", mode="NULLABLE"),
            sf(name="SQL_Access", field_type="STRING", mode="NULLABLE"),
            sf(name="BQ_Access", field_type="STRING", mode="NULLABLE"),
            sf(name="BQ_Account_Used", field_type="STRING", mode="NULLABLE"),
            sf(name="Bytes_Uploaded", field_type="INTEGER", mode="NULLABLE"),
            sf(name="Table_Partitions", field_type="INTEGER", mode="NULLABLE"),
            sf(name="Date_Partitioned", field_type="STRING", mode="NULLABLE"),
            sf(name="Runtime", field_type="FLOAT", mode="NULLABLE")
        ]
        upload_job_details_df = pd.DataFrame(
            data={
                'BQ_Project': [self.job_details['BQ Project']],
                'BQ_Dataset': [self.job_details['BQ Dataset']],
                'BQ_Table': [self.job_details['BQ Table']],
                'Upload_Type': [self.job_details['Upload Type']],
                'Job_Status': [self.job_details['Job Status']],
                'Owner': [self.job_details['Owner']],
                'Run_Date': [self.job_details['Run Date']],
                'Location_On_VM': [self.job_details['Location On VM']],
                'Script_Name': [self.job_details['Script Name']],
                'SQL_Access': [self.job_details['SQL Access']],
                'BQ_Access': [self.job_details['BQ Access']],
                'BQ_Account_Used': [self.job_details['BQ Account Used']],
                'Bytes_Uploaded': [self.job_details['Bytes Uploaded']],
                'Table_Partitions': [self.job_details['Table Partitions']],
                'Date_Partitioned': [self.job_details['Date Partitioned']],
                'Runtime': [self.job_details['Runtime']]
            }
        )
        scopes = ['https://www.googleapis.com/auth/bigquery', 'https://www.googleapis.com/auth/drive.readonly']
        key_path = 'S:/Share_Folder/CsPy/BQ Account'
        bq_key = os.path.join(key_path, 'Job_Details_Key.json')
        bq_credentials = service_account.Credentials.from_service_account_file(bq_key, scopes=scopes)
        upload_job_details_bq_client = Client(project='agile-bonbon-662', credentials=bq_credentials)
        upload_job_details_dataset_ref = DatasetReference(project='agile-bonbon-662', dataset_id='VM_Audit')
        upload_job_details_job_config = LoadJobConfig()
        upload_job_details_job_config.write_disposition = 'WRITE_APPEND'
        upload_job_details_job_config.schema = upload_job_details_schema
        upload_job_details_job_config.skip_leading_rows = 1
        upload_job_details_job_config.source_format = 'CSV'
        save_path = self.save_file_path + "{}.csv"
        upload_job_details_df.to_csv(save_path.format('Upload_Details'), index=False, header=True)
        if not self.setting.testing:
            with open(save_path.format('Upload_Details'), 'rb') as upload_details_file:
                try:
                    table_ref = upload_job_details_dataset_ref.table('VM_Audit')
                    upload_job = upload_job_details_bq_client.load_table_from_file(
                        file_obj=upload_details_file, destination=table_ref, job_config=upload_job_details_job_config)
                    upload_job.result()
                    self.log(upload_job.state)
                except Exception as e:
                    self.log("Table Upload_Details failed to upload to VM_Audit")
                    self.log('Error: {}'.format(upload_job.errors[0]['message']))
                    self.log('Error: {}'.format(upload_job.errors[1]['message']))
                    self.job_details['Error'] = e

            self.log('Removing Upload_Details CSV')
            os.unlink(save_path.format('Upload_Details'))
        else:
            self.log('Testing live not storing results in BQ')

    def send_email(self):
        """
        INTERNAL FUNCTION
        """
        self.job_details['Job Status'] = 'Ran Unsuccessfully'
        if not self.setting.testing and self.vm_status and self.use_account:
            sender = self.account.info['data_team_vm_email']
            receiver = '{0}; {1}'.format(
                self.account.info['data_team_email'],
                self.account.info['email']
            )

            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = 'VM Script: {} Failed to Run.'.format(self.job_details['Script Name'])
            if self.job_details['Job Progress'] == 'Uploading to Big query.':
                if self.job_details['GA Error'] == '':
                    self.job_details['GA Error'] = 'No GA Error'

            message = """
            <p><strong>Time Ran:</strong> {0} <br>
            <strong>Script Owner:</strong> {1} <br><br>
            <strong>The Script located at:</strong> {2}\\{3} <br>
            <strong>The Script failed at:</strong> {4} - {5} <br><br>
            <strong>Error Message:</strong> {6} <br>
            <strong>BQ Error Message:</strong> {7} <br><br>
            For Further Details Please Read The Script Logs On The VM <br>
            <strong>CsPy Version: {8}</p>
            """.format(self.job_details['Run Date'],
                       self.account.info['first_name'] + ' ' + self.account.info['surname'],
                       self.job_details['Location On VM'],
                       self.job_details['Script Name'],
                       self.job_details['Job Portion'],
                       self.job_details['Job Progress'],
                       self.job_details['Error'],
                       self.job_details['GA Error'],
                       self.version
                       )

            msg.attach(MIMEText(message, 'plain'))

            with SMTP(host="fortimail.gslb.thehut.local", port=25) as smtp:
                try:
                    smtp.sendmail(sender, receiver, msg.as_string())
                    self.log('Failed Script Email sent.')
                except SMTPException as error:
                    self.log('Failed Script Email not sent Error: {0}.'.format(error))

        else:
            self.log("Failed Email Alert Not Sent. Only Available On The VM Whilst Using Accounts")


class DownloadJob(BaseJob):
    """
    Desc:
        DownloadJob (class): Class used to initialise an download job and run the download to export data
                      Notes: This will allow the export of data from various databases

    Args:
        query (str): If uploading via SQL or BQ this is the query you wish to run
              Notes: Not needed if you are uploading via a CSV, JSON or DATAFRAME data types

        bq_project (str): The name of the big query project you wish to upload to

        bq_key_path (str): The file path to the folder that your BQ service account is stored
                  Example: "C:/Users/RobinsonJa/Service_Accounts/"

        bq_key_name (str): Name of your BQ service account file
                  Example: "bq_key.json"

        sql_server (str): The connection name of the sql server you wish to read data from
                   Notes: Not needed if you are uploading via BQ, CSV, JSON or DATAFRAME
                   Notes: Not needed if you are using an account and plan on using your default server

        sql_key_path (str): The file path to the folder that your SQL service account is stored
                   Example: "C:/Users/RobinsonJa/Service_Accounts/"
                     Notes: Not needed if you are uploading via BQ, CSV, JSON or DATAFRAME

        sql_key_name (str): Name of your SQL service account file
                   Example: "sql_key.json"
                     Notes: Not needed if you are uploading via BQ, CSV, JSON or DATAFRAME
                     Notes: Not needed if you are using an account and plan on using your default key name

    Optional Args:
        input_data_from (str): Type of data that will be used in the job.
                        Notes: Accepted inputs are SQL, BQ, CSV, JSON, DATAFRAME
                        Notes: Optional but recommended argument

        output_data_type (str): Type of data export that will be used in the job
                         Notes: Accepted inputs are CSV, JSON, DATAFRAME. Defaults to CSV if not supplied
                         Notes: Optional but recommended argument

        save_file_path (str): The file path used to store data files for Upload or Download
                     Example: "C:/Users/RobinsonJa/data/"
                       Notes: If not supplied job will create a temporary DATA folder then is remove after upload
                       Notes: Optional but recommended argument

        save_file_name (str): The name of the file that will saved down if exporting either CSV or JSON
                     Example: "data_file"
                       Notes: If not supplied then the output file with be called "data"
                       Notes: Optional but recommended argument

        account_first_name (str): First name used on the account you wish to use
                           Notes: Used to read the account details for the given first name
                           Notes: Using accounts will require less overall inputs per job

        account_surname (str): Surname used on the account you wish to use
                           Notes: Used to read the account details for the given first name
                           Notes: Using accounts will require less overall inputs per job

        account_file_path (str): The file path to the folder that your account is stored
                        Example: "C:/Users/RobinsonJa/account/"
                          Notes: Not needed if your account file is within the working directory of your script
                          Notes: Not needed on the VM if you have saved the account in the designated folder

    Setting Args:
        set_logging (bool): Set True for console output. Set False for no console output
                     Notes: Defaults to True

        set_clear_save_file_location (bool): Set True to remove any files that match your output file type
                                      Notes: Defaults to False
                                      Notes: This will remove files so ensure your save_file_location is correct

        set_open_file (bool): Set True to open the export file at the end of the script
                       Notes: Defaults to False

        set_testing (bool): Set True when testing on the VM to stop failure emails being sent
                     Notes: Defaults to False

    Raises:
        InputError: When an input is supplied incorrectly
    """

    def __init__(self, query=None, input_data_from=None, output_data_type=None,
                 bq_project=None, bq_key_path=None, bq_key_name=None,
                 sql_server=None, sql_key_path=None, sql_key_name=None, save_file_path=None, save_file_name=None,
                 account_first_name=None, account_surname=None, account_file_path=None,
                 set_logging=None, set_clear_save_file_location=None, set_open_file=None, set_testing=None
                 ):
        super().__init__(query, input_data_from,
                         bq_project, bq_key_path, bq_key_name,
                         sql_server, sql_key_path, sql_key_name, save_file_path,
                         account_first_name, account_surname, account_file_path,
                         set_logging, set_testing)

        # Initialising Download Job
        self.job_details['Job Portion'] = 'Initialising Download Job'
        self.progress_update('Initialising Download Job', print_line=True, print_value=True)
        self.job_type = 'Download'
        self.setting.update(self.job_type, set_clear_save_file_location, None, set_open_file)
        self.output_data_type = output_data_type
        self.save_file_name = save_file_name

        # Determine Input Data Type
        self.progress_update('Searching For Data Type', print_line=True, print_value=True)
        self.get_input_data_type()

        # Load Data Into DataFrame
        self.progress_update('Getting Data From {}'.format(self.input_data_from), print_line=True, print_value=True)
        self.data = self.load_data()

    def get_input_data_type(self):
        """
        INTERNAL FUNCTION
        """
        try:
            self.log('Searching For Input Data Type')
            if self.input_data_from is None:
                self.log('input_data_from Not Provided Reading Inputs To Diagnose Input Data Type')
                if self.query is not None:
                    self.query_classification()
                    self.log('Input Data Type Found: {}'.format(self.input_data_from))

            else:
                if self.input_data_from in ('SQL', 'BQ'):
                    self.log('User Defined Input Data Type Found: {}'.format(self.input_data_from))
                else:
                    self.job_details['Error Message'] = "Variable input_data_from Value \"{}\" Not Recognised".format(
                        self.input_data_from)
                    self.job_details['Solution'] = "Accepted input_data_from Values Are: SQL, BQ"
                    raise InputError(job_progress=self.job_details['Job Progress'],
                                     input_variable_name="input_data_from",
                                     message=self.job_details['Error Message'],
                                     solution=self.job_details['Solution']
                                     )

        except Exception as e:
            if self.sys_exit:
                pass
            else:
                self.job_details['Error'] = str(e)
                self.log('Error: {}'.format(e))
                self.run_script_error(error="Failed To Get Input Data Type",
                                      solution="Check The Script's Logs For Further Detail"
                                      )

        finally:
            self.send_failure_email()

    def load_data(self):
        """
        INTERNAL FUNCTION
        """
        try:
            start_time = dt.datetime.now()
            df = pd.DataFrame()
            if self.input_data_from == 'SQL':
                self.log("Getting SQL Credentials")
                self.get_sql_variables()
                self.log('Reading From SQL Server: {}'.format(self.sql_server))
                self.query = """
                        set ansi_nulls off 
                        set nocount on 
                        set ansi_warnings off
                        """ + self.query
                self.get_sql_connection()
                self.log('Collecting Data...')
                df = pd.read_sql(sql=self.query, con=self.sql_connection)

            elif self.input_data_from == 'BQ':
                self.log("Getting BQ Credentials")
                self.get_bq_variables()
                self.log('Reading From BQ Server: {}'.format(self.bq_project))
                self.get_bq_connection()
                self.log('Collecting Data...')
                df = pd.read_gbq(query=self.query, project_id=self.bq_project, dialect='standard',
                                 credentials=self.bq_credentials)

            end_time = dt.datetime.now()
            self.data_frame_info(start_time, end_time, df)
            return df

        except Exception as e:
            if self.sys_exit:
                pass
            else:
                self.job_details['Error'] = str(e)
                self.log('Error: {}'.format(e))
                self.run_script_error(error="Failed To Load Data",
                                      solution="Check The Script's Logs For Further Detail"
                                      )

        finally:
            self.send_failure_email()

    def run(self):
        """
        Desc:
            run (function): Run the download process for a DownloadJob

        Args:
            self: All variables built within the UploadJob class

        Returns:
            Dataframe - If the output_data_type is set to DATAFRAME
            Save File Path - If the output_data_type is set to CSV or JSON

        Raises:
            No exceptions raised in this function
        """
        try:
            self.job_details['Job Portion'] = 'Running Download Job'
            self.job_details['Error'] = ''
            self.run_error = False
            self.sys_exit = False
            self.progress_update('Creating Download Files', print_line=True, print_value=True)
            if self.output_data_type is None:
                self.log("output_data_type Not Supplied Using Default Out Of CSV")
                self.output_data_type = "CSV"
            elif self.output_data_type not in ('CSV', 'JSON', 'DATAFRAME'):
                self.job_details['Error Message'] = "Variable output_data_type Value \"{}\" Not Recognised".format(
                    self.output_data_type)
                self.job_details['Solution'] = "Accepted output_data_type Values Are: CSV, JSON, DATAFRAME"

                raise InputError(job_progress=self.job_details['Job Progress'],
                                 input_variable_name="output_data_type",
                                 message=self.job_details['Error Message'],
                                 solution=self.job_details['Solution']
                                 )

            if self.output_data_type == 'DATAFRAME':
                self.log("Outputting DATAFRAME")
                return self.data

            if self.output_data_type in ('CSV', 'JSON'):
                if self.setting.clear_data_cache and self.setting.use_user_defined_save_file_path:
                    self.log("Deleting File In Save Location")
                    self.delete_folder_contents(self.output_data_type)

                if self.save_file_name is None:
                    self.save_file_name = "data"

                if right(self.save_file_path, 1) not in ('/', '\\'):
                    self.save_file_path = self.save_file_path + '/'

                self.save_file_name.replace('.csv', '')
                self.save_file_name.replace('.json', '')

                self.save_file_path = self.save_file_path + self.save_file_name + '.{}'.format(
                    self.output_data_type.lower())

                if self.output_data_type == 'CSV':
                    self.log("Saving CSV To: {}".format(self.save_file_path))
                    self.data.to_csv(self.save_file_path, index=False, header=True)

                elif self.output_data_type == 'JSON':
                    self.log("Saving JSON To: {}".format(self.save_file_path))
                    self.data.to_json(self.save_file_path)

                if self.setting.open_file:
                    self.log("Opening Data File")
                    os.system('start "excel" "{}"'.format(self.save_file_path))

                return self.save_file_path

        except Exception as e:
            self.job_details['Error'] = str(e)
            self.log('Error: {}'.format(e))
            self.run_script_error(error="Failed To Export Data",
                                  solution="Check The Script's Logs For Further Detail"
                                  )

        finally:
            self.send_failure_email()


class Account:
    """
    Desc:
        Account (class): Class used to support BaseJob functions

    Args:
        first_name (str): First name of the account you wish to interact with
                   Notes: Needed if you are creating an account file

        surname (str): Surname of the account you wish to interact with
                Notes: Needed if you are creating an account file

    Optional Args:
        file_path (str): The file path to the folder that your account file is stored
                  Example: "C:/Users/RobinsonJa/Service_Accounts/"

        vm_status (bool): True if running via a VM false if not
                   Notes: Only supplied within internal function calls to a class

    Setting Args:
        log_setting (bool): Set to True to performing logging. Set to False to block logging
                     Notes: Only supplied within internal function calls to a class

    Returns:
        No values are returned as this class just creates an Account Variable
    """

    def __init__(self, first_name=None, surname=None, file_path=None, vm_status=False, log_setting=False):
        self.first_name = first_name
        self.surname = surname
        self.file_path = file_path
        self.info = {}
        self.vm_status = vm_status
        self.log_setting = log_setting
        self.use_account = False
        self.load_account()

    def log(self, string):
        """
        INTERNAL FUNCTION
        """
        if self.log_setting:
            print(dt.datetime.now(), ': ', string)

    def load_account(self):
        """
        INTERNAL FUNCTION
        """
        if self.first_name is None and self.surname is None:
            self.log("Account Details Not Supplied Continuing Without Account")
        else:
            self.log("Searching For Account Using {0} {1}".format(self.first_name, self.surname))
            if self.vm_status:
                account_file = 'S:/Share_Folder/CsPy/Accounts/{}_{}.json'

            elif self.file_path is not None:
                account_file = self.file_path + '/{}_{}.json'

            else:
                file = sys.modules['__main__'].__file__
                directory_name, file_name = os.path.split(os.path.abspath(file))
                directory_name = str(directory_name).replace("\\", "/") + "/"
                account_file = directory_name + '{}_{}.json'

            try:
                account_path = account_file.format(self.first_name, self.surname)
                with open(account_path, ) as file:
                    self.log("Account Found")
                    account_data = json.load(file)
                    self.log("Loading Account Details")
                    for i in account_data[0]:
                        self.info['{}'.format(i)] = account_data[0]['{}'.format(i)]
                    self.use_account = True
                    self.log('Using Account: {} {}'.format(self.info['first_name'], self.info['surname']))
                    self.get_team_info()

            except Exception as e:
                self.log('Error: {}'.format(e))
                self.log('Failed To Load Account.')
                self.use_account = False

    def get_team_info(self):
        """
        INTERNAL FUNCTION
        """
        if self.use_account and self.vm_status:
            self.info['key_folder_path'] = None
            self.info['data_team_vm_email'] = None
            team_info_file = "S:/Share_Folder/CsPy/Team Info/Team_Info.json"
            with open(team_info_file, ) as file:
                team_info = json.load(file)
                for i in team_info:
                    if self.info['data_team_id'] == i["data_team_id"]:
                        self.log("Data Team VM Info Found")
                        if i["complete"] == 1:
                            self.log('Updated VM Team Info')
                            self.info['key_folder_path'] = i["key_path_folder"]
                            self.info['data_team_vm_email'] = i["vm_email"]
                            break

                        else:
                            self.log("Data Team VM Info Not Currently Set Up Contact James Robinson To Update This")

    def create_account(self):
        """
        Desc:
            create_account (function): Function used to create an account file

        Args:
            self: All values attached to the class

        Returns:
            Creates a account file with the working directory
        """
        print('=' * 99)
        print('Please provide answers to each request if you do not have the information currently enter: None')
        self.info['first_name'] = input("First Name?\n> ")
        self.info['surname'] = input("Surname?\n> ")
        self.info['email'] = input("Email Address?\n> ")
        self.info['data_team_id'] = input(
            "Data Team?\n 1 = Nutrition Data \n 2 = Nutrition Finance \n 3 = Nutrition Category"
            "\n 4 = Beauty Data \n 5 = Central Marketing \n 6 = DS Logistics \n 7 = Ingenuity \n 8 = Operations \n>")
        self.info['data_team_email'] = input("Data Team DL Email? (EG: DL-Wellbeing-Data@thehutgroup.com) \n>")
        self.info['sql_server'] = input("Default SQL Server? (SQL Server Connection String)\n> ")
        self.info['sql_key'] = input("Default SQL Service Account File Name? (EG: sql_key.json) \n> ")
        self.info['bq_server'] = input("Default Upload BQ Project Name? \n> ")
        self.info['bq_key'] = input("Default BQ Service Account File Name? (EG: bq_key.json) \n> ")
        self.writing()

    def writing(self):
        """
        INTERNAL FUNCTION
        """
        if self.vm_status:
            path = 'S:/Share_Folder/CsPy/Accounts/{}_{}.json'.format(
                self.info['first_name'], self.info['surname'])
        else:
            file = sys.modules['__main__'].__file__
            directory_name, file_name = os.path.split(os.path.abspath(file))
            directory_name = str(directory_name).replace("\\", "/") + "/"
            path = directory_name + '{}_{}.json'.format(self.info['first_name'], self.info['surname'])

        if os.path.exists(path):
            os.remove(path)

        account_info = [
            {
                "first_name": self.info['first_name'],
                "surname": self.info['surname'],
                "email": self.info['email'],
                "data_team_id": self.info['data_team_id'],
                "data_team_email": self.info['data_team_email'],
                "sql_server": self.info['sql_server'],
                "sql_key": self.info['sql_key'],
                "bq_server": self.info['bq_server'],
                "bq_key": self.info['bq_key'],
            }
        ]

        with open(path, 'w') as file:
            json.dump(account_info, file)


class GeneralScriptError(Exception):
    """
    Desc:
        GeneralScriptError (Exception): Exception Raised for general errors that should break the job

    Args:
        job_progress (str): Progress in the script

        message (str): Explanation of the error

        solution (str): Most common way to fix the error
    """

    def __init__(self, job_progress, message, solution):
        self.job_progress = job_progress
        self.message = message
        self.solution = solution
        self.line = '=' * 99
        super().__init__(self)

    def __str__(self):
        return f"""

SCRIPT ERROR!
{self.line}
FAILED DURING: {self.job_progress}
ERROR DETAILS: {self.message}
SOLUTION: {self.solution}
{self.line}
        """


class InputError(Exception):
    """
    Desc:
        InputError (Exception): Exception Raised for errors in the input to download job

    Args:
        job_progress (str): Progress in the script

        input_variable_name (str): Input expression in which the error occurred

        message (str): Explanation of the error

        solution (str): Most common way to fix the error
    """

    def __init__(self, job_progress, input_variable_name, message, solution):
        self.job_progress = job_progress
        self.input_variable_name = input_variable_name
        self.message = message
        self.solution = solution
        self.line = '=' * 99
        super().__init__(self)

    def __str__(self):
        return f"""

INPUT ERROR!
{self.line}
FAILED DURING: {self.job_progress}
FAILED VARIABLE: {self.input_variable_name}
INPUT ERROR: {self.message}
SOLUTION: {self.solution}
{self.line}
        """


class ColumnMissingError(Exception):
    """
    Desc:
        ColumnMissingError (Exception): Exception raised for errors within data_convert and int_convert

    Args:
        missing_column (str): Name of the column that can not be found

        job_progress (str): Progress in the script
    """

    def __init__(self, missing_column, job_progress):
        self.missing_column = missing_column
        self.job_progress = job_progress
        self.line = '=' * 99
        super().__init__(self)

    def __str__(self):
        return f"""
        
COLUMN NOT FOUND ERROR!
{self.line}
FAILED DURING: {self.job_progress}
COLUMN NOT FOUND ERROR: Column name {self.missing_column} is not found
SOLUTION: Make sure column names match the schema provided including case sensitivity
{self.line}
        """
