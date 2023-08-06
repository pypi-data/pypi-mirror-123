# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""Module defining the Task abstract base class which is inherited by the following specific task types:

- IntegrationTask
- AnalyticsTask
- LogicModuleTask
- QueueTask

Also includes the Automation class which contains helper functions.

---------------
IntegrationTask
---------------
Base class used to create integrations between the Switch Automation platform and other platforms, low-level services,
or hardware.

Examples include:
    - Pulling readings or other types of data from REST APIs
    - Protocol Translators which ingest data sent to the platform via email, ftp or direct upload within platform.

-------------
AnalyticsTask
-------------
Base class used to create specific analytics functionality which may leverage existing data from the platform. Each
task may add value to, or supplement, this data and write it back.

Examples include:
    - Anomaly Detection
    - Leaky Pipes
    - Peer Tracking

---------------
LogicModuleTask
---------------
Base class that handles the running, reprocessing and scheduling of the legacy logic modules in a way which enables
integration with other platform functionality.

---------
QueueTask
---------
Base class used to create data pipelines that are fed via a queue.

----------
Automation
----------
This class contains the helper methods used to register, deploy, and test the created tasks. Additional helper functions
 for retrieving details of existing tasks on the Switch Automation platform are also included in this module.

"""
import enum
import sys
# import re
import pandas
import requests
import inspect
import uuid
import logging
import datetime
import json
from typing import List
from abc import ABC, abstractmethod
from azure.servicebus import ServiceBusClient, ServiceBusReceiveMode  # , ServiceBusMessage
from .._utils._utils import _is_valid_regex, ApiInputs, generate_password, _column_name_cap, DataFeedFileProcessOutput
from .._utils._constants import (api_prefix, argus_prefix, EXPECTED_DELIVERY, DEPLOY_TYPE, MAPPING_ENTITIES,
                                 QUEUE_NAME, ERROR_TYPE)
from .._utils._platform import _get_connection_string
from io import StringIO

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)
formatter = logging.Formatter('%(asctime)s  switch_api.%(module)s.%(funcName)s  %(levelname)s: %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')
consoleHandler.setFormatter(formatter)


# Base Definitions in Switch package
class Task(ABC):
    """An Abstract Base Class called Task.

    Attributes
    ----------
    id : uuid.UUID
        Unique identifier of the task. This is an abstract property that needs to be overwritten when sub-classing.
        A new unique identifier can be created using uuid.uuid4()
    description : str
        Brief description of the task
    mapping_entities : List[MAPPING_ENTITIES]
        The type of entities being mapped. An example is:

        ``['Installations', 'Devices', 'Sensors']``
    author : str
        The author of the task.
    version : str
        The version of the task.

    """

    @property
    @abstractmethod
    def id(self) -> uuid.UUID:
        """Unique identifier of the task. Create a new unique identifier using uuid.uuid4() """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Brief description of the task"""
        pass

    @property
    @abstractmethod
    def mapping_entities(self) -> List[MAPPING_ENTITIES]:
        """The type of entities being mapped."""
        pass

    @property
    @abstractmethod
    def author(self) -> str:
        """"The author of the task."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """The version of the task"""
        pass


class IntegrationTask(Task):
    """Integration Task

    This class is used to create integrations that post data to the Switch Automation platform.


    Only one of the following methods should be implemented per class, based on the type of integration required:

    - process_file()
    - process_stream()
    - process()

    """

    @abstractmethod
    def process_file(self, api_inputs: ApiInputs, file_path_to_process: str):
        """Method to be implemented if a file will be processed by the Integration Task.

        The method should contain all code used to cleanse, reformat & post the data contained in the file.

        Parameter
        _________
        api_inputs : ApiInputs
            object returned by call to initialize()
        file_path_to_process : str
            the file path

        """
        pass

    @abstractmethod
    def process_stream(self, api_inputs: ApiInputs, stream_to_process):
        """Method to be implemented if data received via stream

        The method should contain all code used to cleanse, reformat & post the data received via the stream.

        Parameters
        __________
        api_inputs: ApiInputs
            object returned by call to initialize()
        stream to process :
            details of the stream to be processed.
        """
        pass

    @abstractmethod
    def process(self, api_inputs: ApiInputs, integration_settings: dict):
        """Method to be implemented if data

        The method should contain all code used to cleanse, reformat & post the data pulled via the integration.

        Parameters
        __________
        api_inputs: ApiInputs
            object returned by call to initialize()
        integration_settings : dict
            Any settings required to be passed to the integration to run. For example, username & password, api key,
            auth token, etc.

        """
        pass


class QueueTask(Task):
    """Integration Task

    This class is used to create integrations that post data to the Switch Automation platform using a Queue as the
    data source.

    Only one of the following methods should be implemented per class, based on the type of integration required:

    - process_file()
    - process_stream()
    - process()

    """

    @property
    @abstractmethod
    def queue_name(self) -> str:
        """The name of the queue to receive Data .. Name will actually be constructed as {ApiProjectId}_{queue_name} """
        pass

    @property
    @abstractmethod
    def maximum_message_count_per_call(self) -> int:
        """ The maximum amount of messages which should be passed to the process_queue at any one time 
            set to zero to consume all
        """
        pass

    @abstractmethod
    def start(self, api_inputs: ApiInputs):
        """Method to be implemented if a file will be processed by the QueueTask Task.    
        This will run once at the start of the processing and should contain     

        """
        pass

    @abstractmethod
    def process_queue(self, api_inputs: ApiInputs, messages: List):
        """Method to be implemented if a file will be processed by the QueueTask Task.

        The method should contain all code used to consume the messages

        Parameter
        _________
        api_inputs : ApiInputs
            object returned by call to initialize()
        messages:List)
            list of serialized json strings which have been consumed from the queue

        """
        pass


class AnalyticsTask(Task):

    @abstractmethod
    def start(self, api_inputs: ApiInputs, analytics_settings: dict):
        """Start.

        The method should contain all code used by the task.

        Parameters
        __________
        api_inputs : ApiInputs
            the object returned by call to initialize()
        analytics_settings : dict
            any setting required by the AnalyticsTask

        """
        pass


class LogicModuleTask(Task):

    @abstractmethod
    def start(self, start_date_time: datetime.date, end_date_time: datetime.date, installation_id: uuid.UUID,
              share_tag_group: str, share_tags: list):
        pass

    # Needs to be implemented into the deploy_on_timer


class RunAt(enum.Enum):
    """ """
    Every15Minutes = 1
    Every1Hour = 3
    EveryDay = 4
    EveryWeek = 5


class Automation:
    """Automation class defines the methods used to register and deploy tasks. """

    @staticmethod
    def run_queue_task(task: QueueTask, api_inputs: ApiInputs, consume_all_messages: bool = False):
        """Runs a Queue Task when in Development Mode
        
        The Queue Name should ideally be a testing Queue as messages will be consumed

        Parameters
        ----------
        task : QueueTask
            The custom QueueTask instance created by the user.
        api_inputs : ApiInputs
            Object returned by initialize() function.
        consume_all_messages : bool, default=False
            Consume all messages as they are read.

        Returns
        -------
        bool
            indicating whether the call was successful

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return False

        if not issubclass(type(task), QueueTask):
            logger.error(
                "Driver must be an implementation of the QueueTask (Task).")
            return False

        logger.info("Running queue for  %s (%s) using queue name: %s", str(type(task).__name__), str(task.id),
                    str(task.queue_name))

        task.start(api_inputs)

        message_count = 0
        with ServiceBusClient.from_connection_string(_get_connection_string(
                api_inputs=api_inputs, account="Argus")) as client:
            with client.get_queue_receiver(task.queue_name,
                                           receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE) as receiver:
                while True:
                    messages = []
                    received_message_array = receiver.receive_messages(
                        max_message_count=task.maximum_message_count_per_call, max_wait_time=2)
                    for message in received_message_array:
                        messages.append(str(message))
                        message_count += 1

                    if len(received_message_array) == 0:
                        break

                    task.process_queue(api_inputs, messages)

                    if consume_all_messages == False:
                        break
        logger.info('Total messages consumed: %s', str(message_count))

    @staticmethod
    def reserve_instance(task: Task, api_inputs: ApiInputs, data_feed_id: uuid.UUID, minutes_to_reserve: int = 10):
        """Reserve a testing instance.

        Reserves a testing instance for the `driver`.

        Parameters
        ----------
        task : Task
            The custom Driver class created by the user.
        api_inputs : ApiInputs
            Object returned by initialize() function.
        data_feed_id : uuid.UUID
            The unique identifier of the data feed being tested.
        minutes_to_reserve : int, default = 10
                The duration in minutes that the testing instance will be reserved for (Default value = 10).

        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the details of the reserved testing instance.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        logger.info("Reserving a testing instance for %s (%s) on Data Feed Id (%s). ", str(type(task).__name__),
                    str(task.id), str(data_feed_id))

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        url = argus_prefix + "ReserveInstance/" + str(data_feed_id) + "/" + str(minutes_to_reserve)

        response = requests.request("GET", url, timeout=20, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text, typ="Series")

        return df

    @staticmethod
    def register_task(task):
        """Register the task.

        Registers the task that was defined.

        Parameters
        ----------
        task : Task
            An instance of the custom class created from the Abstract Base Class `Task` or its abstract sub-classes:
            `IntegrationTask`, `AnalyticsTask`, `LogicModuleTask`.

        Returns
        -------
        pandas.DataFrame

        """

        if not issubclass(type(task), Task):
            logger.error(
                "Driver must be an implementation of the Abstract Base Class (Task).")
            return False

        base_class = ''
        if issubclass(type(task), IntegrationTask):
            base_class = 'IntegrationTask'
        elif issubclass(type(task), LogicModuleTask):
            base_class = 'LogicModuleTask'
        elif issubclass(type(task), AnalyticsTask):
            base_class = 'AnalyticsTask'

        if base_class == '':
            logger.error(
                'Task must be an implementation of one of the Task sub-classes: AnalyticsTask, IntegrationTask or '
                'LogicModule.')
            return pandas.DataFrame()

        if type(task.mapping_entities) != list:
            logger.error('The mapping_entities parameter must have type = list. ')
            return pandas.DataFrame()
        elif not set(task.mapping_entities).issubset(set(MAPPING_ENTITIES.__args__)):
            logger.error('mapping_entities property must be a list containing one of the allowed values defined by the '
                         'MAPPING_ENTITIES literal: %s', MAPPING_ENTITIES.__args__)
            return pandas.DataFrame()

        logger.info("Registering %s (%s) to the Switch Driver Library: ", str(type(task).__name__), str(task.id))

        json_payload_verify = {
            "driverId": str(task.id),
            "name": type(task).__name__
        }

        url = api_prefix + "Automation/VerifyRegisterDriver"
        response = requests.post(url, json=json_payload_verify)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif response.text == "Failed":
            logger.error("This Driver Guid is already associated with a Driver with a Different Name.")
            return response_status, pandas.DataFrame()

        json_payload = {
            "driverId": str(task.id),
            "name": type(task).__name__,
            "specification": task.description,
            "mappingEntities": task.mapping_entities,
            "scriptCode": Automation._get_task_code(task),
            "baseClass": base_class
        }

        url = api_prefix + "Automation/RegisterDriver"

        response = requests.post(url, json=json_payload)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text)
        df.columns = _column_name_cap(df.columns)

        return df

    @staticmethod
    def list_tasks(api_inputs: ApiInputs, search_name_pattern: str = '*'):
        """Get a list of the registered tasks.

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize() function.
        search_name_pattern : str, optional
            A pattern that should be used as a filter when retrieving the list of deployed drivers
            (Default value = '*').

        Returns
        -------
        pandas.DataFrame
            Dataframe containing the registered tasks.

        """
        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        url = api_prefix + "Automation/ListDrivers/" + search_name_pattern

        response = requests.request("GET", url, timeout=20, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text)
        df = df.drop(columns=['driverId'])
        df.columns = _column_name_cap(df.columns)

        return df

    @staticmethod
    def deploy_as_email_data_feed(task, api_inputs: ApiInputs, expected_delivery: EXPECTED_DELIVERY,
                                  email_subject_regex: str, email_address_domain='switchautomation.com',
                                  queue_name: QUEUE_NAME = 'task'):
        """Deploy task as an email data feed.

        Deploys the created `task` as an email data feed. This allows the driver to ingest data sent via email. The
        data must be sent to data@switchautomation.com to be processed. If it is sent to another email address, the task
        will not be run.

        Parameters
        ----------
        task : Task
            The custom driver class created from the Abstract Base Class `Task`
        api_inputs : ApiInputs
            Object returned by initialize() function.
        expected_delivery : EXPECTED_DELIVERY
            The expected delivery frequency.
        email_subject_regex : str
            Regex expression used to parse the email subject line to determine which driver the received file will
            be processed by (Default value = '').
        email_address_domain : str, default='switchautomation.com'
            The email domain, without the @ symbol, of the sender (Default value = 'SwitchAutomation.com').
        queue_name : QUEUE_NAME, optional
            The name of queue (Default value = 'task').

        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the details of the deployed email data feed.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        logger.info('Deploy %s (%s) as a data feed for ApiProjectID: %s', type(task).__name__, str(task.id),
                    api_inputs.api_project_id)

        if not _is_valid_regex(email_subject_regex):
            logger.error("%s is not valid regex.", email_subject_regex)
            return pandas.DataFrame()

        if email_address_domain == "switchautomation.com":
            logger.info("Emails can only be received from the %s domain.", email_address_domain)

        if "@" in email_address_domain:
            logger.error("Do not include the @ in the email_address_domain parameter. ")
            return pandas.DataFrame()

        if not set([expected_delivery]).issubset(set(EXPECTED_DELIVERY.__args__)):
            logger.error('expected_delivery parameter must be set to one of the allowed values defined by the '
                         'EXPECTED_DELIVERY literal: %s', EXPECTED_DELIVERY.__args__)
            return pandas.DataFrame()

        if not set([queue_name]).issubset(set(QUEUE_NAME.__args__)):
            logger.error('queue_name parameter must be set to one of the allowed values defined by the '
                         'QUEUE_NAME literal: %s', QUEUE_NAME.__args__)
            return pandas.DataFrame()

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        inbox_container = "data-exchange"
        payload = {
            "driverId": str(task.id),
            "name": 'Feed Settings for ' + type(task).__name__,
            "feedType": ",".join(task.mapping_entities),
            "expectedDelivery": expected_delivery,
            "sourceType": "email",
            "queueName": queue_name,
            "email": {
                "emailAddressDomain": email_address_domain,
                "emailSubjectRegex": email_subject_regex,
                "container": inbox_container
            }
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Automation/DeployTask"

        response = requests.post(url, json=payload, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text, typ='Series').to_frame().T
        df.columns = _column_name_cap(df.columns)

        return df

    @staticmethod
    def deploy_as_ftp_data_feed(task, api_inputs: ApiInputs, ftp_user_name, ftp_password,
                                expected_delivery: EXPECTED_DELIVERY, queue_name: QUEUE_NAME = 'task'):
        """Deploy the custom driver as an FTP data feed

        Deploys the custom driver to receive data via an FTP data feed. Sets the `ftp_user_name` & `ftp_password` and
        the `expected_delivery` of the file.

        Parameters
        ----------
        task : Task
            The custom driver class created from the Abstract Base Class 'Task'
        api_inputs : ApiInputs
            Object returned by the initialize() function.
        ftp_user_name : str
            The user_name to be used by the ftp service to authenticate delivery of the data feed.
        ftp_password : str
            The password to be used by the ftp service for the given `ftp_user_name` to authenticate delivery of the
            data feed.
        expected_delivery : EXPECTED_DELIVERY
            The expected delivery frequency of the data.
        queue_name : QUEUE_NAME, default = 'task'
            The queue name (Default value = 'task').

        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the details of the deployed ftp data feed.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        if not set([expected_delivery]).issubset(set(EXPECTED_DELIVERY.__args__)):
            logger.error('expected_delivery parameter must be set to one of the allowed values defined by the '
                         'EXPECTED_DELIVERY literal: %s', EXPECTED_DELIVERY.__args__)
            return pandas.DataFrame()

        if not set([queue_name]).issubset(set(QUEUE_NAME.__args__)):
            logger.error('queue_name parameter must be set to one of the allowed values defined by the '
                         'QUEUE_NAME literal: %s', QUEUE_NAME.__args__)
            return pandas.DataFrame()

        logger.info('Deploy %s (%s) as a data feed for ApiProjectID: %s', type(task).__name__, str(task.id),
                    api_inputs.api_project_id)

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        inbox_container = "data-exchange"
        payload = {
            "driverId": str(task.id),
            "name": 'Feed Settings for ' + type(task).__name__,
            "feedType": ",".join(task.mapping_entities),
            "expectedDelivery": expected_delivery,
            "sourceType": "ftp",
            "queueName": queue_name,
            "ftp": {
                "ftpUserName": ftp_user_name,
                "ftpPassword": ftp_password,
                "container": inbox_container
            }
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Automation/DeployTask"

        response = requests.post(url, json=payload, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text, typ='Series').to_frame().T
        df.columns = _column_name_cap(df.columns)

        return df

    @staticmethod
    def deploy_as_upload_data_feed(task, api_inputs: ApiInputs, expected_delivery: EXPECTED_DELIVERY,
                                   queue_name: QUEUE_NAME = 'task'):
        """Deploy the custom driver as a REST API end point Datafeed.

        Parameters
        ----------
        task : Task
            The custom driver class created from the Abstract Base Class 'Driver'
        api_inputs : ApiInputs
            Object returned by the initialize() function.
        expected_delivery : EXPECTED_DELIVERY
            The expected delivery frequency of the data.
        queue_name : QUEUE_NAME, optional
            The queue name (Default value = 'task').


        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the details of the deployed https endpoint data feed.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        if not set([expected_delivery]).issubset(set(EXPECTED_DELIVERY.__args__)):
            logger.error('expected_delivery parameter must be set to one of the allowed values defined by the '
                         'EXPECTED_DELIVERY literal: %s', EXPECTED_DELIVERY.__args__)
            return pandas.DataFrame()

        if not set([queue_name]).issubset(set(QUEUE_NAME.__args__)):
            logger.error('queue_name parameter must be set to one of the allowed values defined by the '
                         'QUEUE_NAME literal: %s', QUEUE_NAME.__args__)
            return pandas.DataFrame()

        logger.info('Deploy %s (%s) as a data feed for ApiProjectID: %s', type(task).__name__, str(task.id),
                    api_inputs.api_project_id)

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        # inbox_container = "data-exchange"
        payload = {
            "driverId": str(task.id),
            "name": 'Feed Settings for ' + type(task).__name__,
            "feedType": ",".join(task.mapping_entities),
            "expectedDelivery": expected_delivery,
            "sourceType": "upload",
            "queueName": queue_name,
            "upload": {
                "placeholder": ""
            },
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Automation/DeployTask"

        response = requests.post(url, json=payload, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(StringIO(response.text), typ='Series').to_frame().T
        df.columns = _column_name_cap(df.columns)

        return df

    @staticmethod
    def deploy_on_timer(task, api_inputs: ApiInputs, cron_schedule, expected_delivery: EXPECTED_DELIVERY,
                        queue_name: QUEUE_NAME = "task", settings: dict = None):
        """Deploy driver to run on timer.

        Parameters
        ----------
        task : Task
            The custom driver class created from the Abstract Base Class `Driver`.
        api_inputs : ApiInputs
            Object returned by initialize.initialize() function
        cron_schedule :
            Cron object containing the required schedule for the driver to be run.
        expected_delivery : EXPECTED_DELIVERY
            The expected delivery frequency.
        queue_name : QUEUE_NAME, optional
            The queue name (Default value = 'task').
        settings : dict, Optional
                List of settings used to deploy the driver. For example, may contain the user_name and password
                required to authenticate calls to a third-party API (Default value = None).

        Returns
        -------
        pandas.Dataframe
            A dataframe containing the details of the deployed data feed.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        if not set([expected_delivery]).issubset(set(EXPECTED_DELIVERY.__args__)):
            logger.error('expected_delivery parameter must be set to one of the allowed values defined by the '
                         'EXPECTED_DELIVERY literal: %s', EXPECTED_DELIVERY.__args__)
            return pandas.DataFrame()

        if not set([queue_name]).issubset(set(QUEUE_NAME.__args__)):
            logger.error('queue_name parameter must be set to one of the allowed values defined by the '
                         'QUEUE_NAME literal: %s', QUEUE_NAME.__args__)
            return pandas.DataFrame()

        if len(cron_schedule.split(' ')) != 7:
            logger.error("cron_schedule parameter must be in the format * * * * * *")
            return pandas.DataFrame()

        # # TODO - discuss whether this is required since we added the Literal EXPECTED_DELIVERY
        # expected_deliveries = re.findall(r'[A-Za-z]+|\d+', expected_delivery)
        # if len(expected_deliveries) != 2 or expected_deliveries[0].isnumeric() is not True:
        #     logger.error("Run At parameter must take the form of a number followed by a time type. ")
        #     return pandas.DataFrame()
        #
        # time_type = expected_deliveries[1].lower()[:3]
        # if time_type != 'min' and time_type != 'hour' and time_type != 'day':
        #     logger.error("The expected_delivery time type must start with one of: min, hour, day. ")
        #     return pandas.DataFrame()

        logger.info('Deploy %s (%s) on timer for ApiProjectID: %s and schedule: %s.', type(task).__name__,
                    str(task.id), api_inputs.api_project_id, cron_schedule)
        logger.info('Feed Type is %s', str(task.mapping_entities))
        logger.info('Settings to be passed to the driver on start are: %s', str(settings))

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        payload = {
            "driverId": str(task.id),
            "name": 'Timer Settings for ' + type(task).__name__,
            "feedType": ",".join(task.mapping_entities),
            "expectedDelivery": expected_delivery,
            "sourceType": "BlobFolder",
            "queueName": queue_name,
            "timer": {
                "cronSchedule": cron_schedule
            },
            "settings": settings
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Automation/DeployTask"

        response = requests.post(url, json=payload, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text, typ='Series').to_frame().T
        df.columns = _column_name_cap(df.columns)

        return df

    @staticmethod
    def cancel_deploy(task, api_inputs: ApiInputs, deploy_type: DEPLOY_TYPE = 'timer'):
        """Deploy driver to run on timer.

        Parameters
        ----------
        task : Task
            The custom task class created from the Abstract Base Class `Task`.
        api_inputs : ApiInputs
            Object returned by initialize.initialize() function
        deploy_type : DEPLOY_TYPE, optional
            One of the deploy types defined by the DEPLOY_TYPE literal (Default value = 'timer')


        Returns
        -------
        str
            A string containing the response text.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        if str(deploy_type) != 'timer':
            logger.error('The cancel_deploy() function currently only works for data feeds deployed on timer. ')
            return

        if not set([deploy_type]).issubset(set(DEPLOY_TYPE.__args__)):
            logger.error('deploy_type parameter must be set to one of the allowed values defined by the '
                         'DEPLOY_TYPE literal: %s', DEPLOY_TYPE.__args__)
            return pandas.DataFrame()

        logger.info('Cancel deploy %s (%s) on timer for ApiProjectID: %s', type(task).__name__,
                    str(task.id), api_inputs.api_project_id)
        logger.info('Feed Type is %s', str(task.mapping_entities))

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        # payload = {}

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Automation/CancelTask/" + \
            deploy_type + "/" + str(task.id)

        response = requests.get(url, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text, typ='Series').to_frame().T
        df.columns = _column_name_cap(df.columns)

        return df

    @staticmethod
    def list_deployments(api_inputs: ApiInputs, search_name_pattern='*'):
        """Retrieve list of deployed drivers.

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize.initialize() function
        search_name_pattern : str
                A pattern that should be used as a filter when retrieving the list of deployed drivers
                (Default value = '*').

        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the drivers deployed for the given ApiProjectID that match the `search_name_pattern`.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Automation/ListDeployments/" + \
            search_name_pattern

        response = requests.request("GET", url, timeout=20, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text)
        df.columns = _column_name_cap(df.columns)
        return df

    @staticmethod
    def list_data_feed_history(api_inputs: ApiInputs, data_feed_id: uuid.UUID, top_count: int = 10):
        """Retrieve data feed history

        Retrieves the `top_count` records for the given `data_feed_id`.

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize.initialize() function
        data_feed_id : uuid.UUID
            The unique identifier for the data feed that history should be retrieved for.
        top_count : int, default = 10
            The top record count to be retrieved. (Default value = 10).

        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the `top_count` history records for the given `data_feed_id`.

        """

        if data_feed_id is None or data_feed_id == '':
            logger.error('The data_feed_id parameter must be provided. ')
            return

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + \
            "/Automation/ListDataFeedsHistory/" + str(data_feed_id) + "/" + str(top_count)

        response = requests.request("GET", url, timeout=20, headers=headers)

        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text)
        df.columns = _column_name_cap(df.columns)

        return df

    @staticmethod
    def data_feed_history_process_output(api_inputs: ApiInputs, data_feed_id: uuid.UUID = None,
                                         data_feed_file_status_id: uuid.UUID = None, row_number: int = None):
        """Retrieve data feed history process output

        Retrieves the `top_count` records for the given `data_feed_id`.

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize.initialize() function
        data_feed_id : uuid.UUID, default = None
            The unique identifier for the data feed that output should be retrieved for. This parameter works with the
            `row_number`
        data_feed_file_status_id : uuid.UUID, default = None
            The unique identifier for the data feed history should be retrieved for. This UUID can be retrieved from
            the list_data_feed_history() method.
        row_number: int, default = 0
            The row number from the list_data_feed_history method. It can be used in place of the file_status_id. Use
            row_number=0 to retrieve the most recent process.

        Returns
        -------
        log : str
            Containing the full print and output log for the process

        """

        if data_feed_id is None and data_feed_file_status_id is None:
            logger.error('Must supply either the data_feed_id + row_number, or the file_status_id')
            return
        elif data_feed_id is not None and data_feed_file_status_id is None and row_number is None:
            logger.error('When supplying the data_feed_id, you must also provide the row_number to retrieve. ')
            return
        elif data_feed_id is None and data_feed_file_status_id is not None and row_number is not None:
            logger.error('Please supply either the data_feed_id + row_number, or the file_status_id. ')
            return
        elif data_feed_id is not None and data_feed_file_status_id is not None and row_number is not None:
            logger.error('Please supply either the data_feed_id + row_number, or the file_status_id. ')
            return
        elif data_feed_id is not None and data_feed_file_status_id is not None and row_number is None:
            logger.error('Please supply either the data_feed_id + row_number or the file_status_id. ')
            return

        if row_number is None:
            row_number = -1

        if data_feed_id is None:
            data_feed_id = '00000000-0000-0000-0000-000000000000'

        if data_feed_file_status_id is None:
            data_feed_file_status_id = '00000000-0000-0000-0000-000000000000'

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + \
            "/Automation/DataFeedsProcessOutput/" + str(data_feed_id) + "/" + str(data_feed_file_status_id) + "/" + \
            str(row_number)

        response = requests.request("GET", url, timeout=20, headers=headers)

        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        data_feed_file_process_output = json.loads(response.text, object_hook=lambda d: DataFeedFileProcessOutput(
            data_feed_id=d['dataFeedId'], data_feed_file_status_id=d['fileStatusId'],
            client_tracking_id=d['clientTrackingId'],
            source_type=d['sourceType'], file_name=d['fileName'], file_received=d['fileReceived'],
            file_process_status=d['fileProcessStatus'], file_process_status_change=d['fileProcessStatusChange'],
            process_started=d['processStarted'], process_completed=d['processCompleted'],
            minutes_since_received=d['minutesSinceReceived'], minutes_since_processed=d['minutesSinceProcessed'],
            file_size=d['fileSize'], log_file_path=d['logFile'], output=d['output'], error=d['error']))

        return data_feed_file_process_output

    @staticmethod
    def data_feed_history_process_errors(api_inputs: ApiInputs, data_feed_id: uuid.UUID,
                                         data_feed_file_status_id: uuid.UUID):
        """Retrieve the unique error types for a given data feed file.

        Retrieves the distinct error types present for the given `data_feed_id` and `data_feed_file_status_id`.

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize.initialize() function
        data_feed_id : uuid.UUID
            The unique identifier for the data feed that errors should be retrieved for.
        data_feed_file_status_id : uuid.UUID
            The unique identifier for the file processed for a given data feed that errors should be retrieved for.

        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the distinct error types present for the given data_feed_file_status_id.

        """

        if data_feed_id == '' or data_feed_file_status_id == '':
            logger.error('The data_feed_id and data_feed_file_status_id parameters must be provided. ')
            return

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + \
            "/Automation/DataFeedsProcessErrors/" + str(data_feed_id) + "/" + str(data_feed_file_status_id)

        response = requests.request("GET", url, timeout=20, headers=headers)

        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text)
        df.columns = _column_name_cap(df.columns)

        return df

    @staticmethod
    def data_feed_history_errors_by_type(api_inputs: ApiInputs, data_feed_id: uuid.UUID,
                                         data_feed_file_status_id: uuid.UUID, error_type: ERROR_TYPE):
        """Retrieve the encountered errors for a given error type, data feed & file.

        Retrieves the errors identified for a given `error_type` for the `data_feed_id` and `data_feed_file_status_id`.

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize.initialize() function
        data_feed_id : uuid.UUID
            The unique identifier for the data feed that errors should be retrieved for.
        data_feed_file_status_id
            The unique identifier for the data feed that errors should be retrieved for.
        error_type: ERROR_TYPE
            The error type of the structured logs to be retrieved.

        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the errors identified for the given `data_feed_file_status_id`.

        """

        if (data_feed_id == '' or data_feed_file_status_id == '' or data_feed_id is None or
                data_feed_file_status_id is None):
            logger.error('The data_feed_id and data_feed_file_status_id parameters must be provided. ')
            return

        if not set([error_type]).issubset(set(ERROR_TYPE.__args__)):
            logger.error('error_type parameter must be set to one of the allowed values defined by the '
                         'ERROR_TYPE literal: %s', ERROR_TYPE.__args__)
            return pandas.DataFrame()

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + \
            "/Automation/DataFeedsProcessGetErrorsByType/" + str(data_feed_id) + "/" + str(data_feed_file_status_id) \
            + "/" + str(error_type)

        response = requests.request("GET", url, timeout=20, headers=headers)

        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_csv(StringIO(response.text), sep=",", error_bad_lines=False)
        return df

    @staticmethod
    def _get_task_code(task):
        """

        Parameters
        ----------
        task : Task
            The custom driver class created from the Abstract Base Class `Task`.

        Returns
        -------
        driver_code : str
            The code used to create the `task`

        """
        task_type = type(task)
        task_code = ''
        parent_module = inspect.getmodule(task_type)
        for codeLine in inspect.getsource(parent_module).split('\n'):
            if codeLine.startswith('import ') or codeLine.startswith('from '):
                task_code += codeLine + '\n'

        task_code += '\n'
        task_code += inspect.getsource(task_type)
        task_code += ''
        task_code += 'task = ' + task_type.__name__ + '()'

        return task_code
