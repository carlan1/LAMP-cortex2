# coding: utf-8

"""
    LAMP Platform

    The LAMP Platform API.

    The version of the OpenAPI document: 1.0.0
    Contact: team@digitalpsych.org
"""

from __future__ import absolute_import
import os
import boto3

#__version__ = "develop"

# import apis into sdk package
from LAMP2.api import APIApi
from LAMP2.api.activity_api import ActivityApi
from LAMP2.api.activity_event_api import ActivityEventApi
from LAMP2.api.activity_spec_api import ActivitySpecApi
from LAMP2.api.credential_api import CredentialApi
from LAMP2.api.participant_api import ParticipantApi
from LAMP2.api.researcher_api import ResearcherApi
from LAMP2.api.sensor_api import SensorApi
from LAMP2.api.sensor_event_api import SensorEventApi
from LAMP2.api.sensor_spec_api import SensorSpecApi
from LAMP2.api.study_api import StudyApi
from LAMP2.api.type_api import TypeApi

# import ApiClient
from LAMP2.api_client import ApiClient

# import Configuration
from LAMP2.configuration import Configuration

# import exceptions
from LAMP2.exceptions import LAMPException
from LAMP2.exceptions import ApiTypeError
from LAMP2.exceptions import ApiValueError
from LAMP2.exceptions import ApiKeyError
from LAMP2.exceptions import ApiException

# import models into sdk package
from LAMP2.models.access_citation import AccessCitation
from LAMP2.models.activity import Activity
from LAMP2.models.activity_event import ActivityEvent
from LAMP2.models.activity_spec import ActivitySpec
from LAMP2.models.credential import Credential
from LAMP2.models.document import Document
from LAMP2.models.duration_interval import DurationInterval
from LAMP2.models.duration_interval_legacy import DurationIntervalLegacy
from LAMP2.models.dynamic_attachment import DynamicAttachment
from LAMP2.models.error import Error
from LAMP2.models.metadata import Metadata
from LAMP2.models.participant import Participant
from LAMP2.models.researcher import Researcher
from LAMP2.models.sensor import Sensor
from LAMP2.models.sensor_event import SensorEvent
from LAMP2.models.sensor_spec import SensorSpec
from LAMP2.models.study import Study
from LAMP2.models.temporal_slice import TemporalSlice

API = APIApi()
Type = TypeApi()
Credential = CredentialApi()
Researcher = ResearcherApi()
Study = StudyApi()
Participant = ParticipantApi()
Activity = ActivityApi()
ActivitySpec = ActivitySpecApi()
ActivityEvent = ActivityEventApi()
Sensor = SensorApi()
SensorSpec = SensorSpecApi()
SensorEvent = SensorEventApi()

def connect(access_key=None, 
        secret_key=None, 
        server_address=None, 
        s3_access_key=None, 
        s3_secret_key=None,
        archive=False,
        s3_region_name='us-east-2'):
    if archive and s3_access_key is None and s3_secret_key is None:
        s3_access_key = os.getenv('S3_ACCESS_KEY')
        s3_secret_key = os.getenv('S3_SECRET_KEY')
    if access_key is None and secret_key is None:
        access_key = os.getenv('LAMP_ACCESS_KEY')
        secret_key = os.getenv('LAMP_SECRET_KEY')
    if server_address is None:  # let arg override environmental var
        server_address = os.getenv('LAMP_SERVER_ADDRESS', 'api.lamp.digital')
    if access_key is None or secret_key is None:
        raise TypeError("connect() requires 2 positional arguments: 'access_key' and 'secret_key', unless environmental variables 'LAMP_ACCESS_KEY' and 'LAMP_SECRET_KEY' are provided")

    if archive:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=s3_access_key,
            aws_secret_access_key=s3_secret_key,
            region_name=s3_region_name
            )
        print("Successfully accessed the archive.")
    else:
        s3_client = None
        
    client = ApiClient(Configuration(host=f"https://{server_address}", username=access_key, password=secret_key))

    global API
    global Type
    global Credential
    global Researcher
    global Study
    global Participant
    global Activity
    global ActivitySpec
    global ActivityEvent
    global Sensor
    global SensorSpec
    global SensorEvent

    API = APIApi(client)
    Type = TypeApi(client)
    Credential = CredentialApi(client)
    Researcher = ResearcherApi(client)
    Study = StudyApi(client)
    Participant = ParticipantApi(client)
    Activity = ActivityApi(client)
    ActivitySpec = ActivitySpecApi(client)
    ActivityEvent = ActivityEventApi(client)
    Sensor = SensorApi(client)
    SensorSpec = SensorSpecApi(client)
    SensorEvent = SensorEventApi(client, s3_client=s3_client)