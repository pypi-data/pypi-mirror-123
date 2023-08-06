import datetime
import json
import logging
import os
import pathlib
import sys
import tempfile

import google.cloud.logging
import requests

import dcyd.gcl_patch as gcl_patch
import dcyd.utils as utils


class ExtractMsgFormatter(logging.Formatter):
    def format(self, record):
        return record.msg


def request_service_account_key(*, project_credentials: dict = utils.get_project_credentials()):
    '''
    Request the latest GCP service account key and write it to a temp file.
    '''
    if not project_credentials.get('project_id'):
        utils.report_client_error('Project ID not found.')
        return None

    if not project_credentials.get('project_access_token'):
        utils.report_client_error('Project access token not found.')
        return None

    response = requests.post(
        utils.api_url('/service_account_key'),
        json=project_credentials,
    )

    if not response.ok:
        utils.report_client_error(f'Failed to request service credentials: {response.text}')
        return None

    key_file_path = os.path.join(tempfile.gettempdir(), 'dcyd_gcsak.json')
    pathlib.Path(key_file_path).write_text(response.text)
    return key_file_path


def get_stderr_logger() -> logging.Logger:
    '''
    Initialize a logger writes to stderr
    '''
    logger = logging.getLogger('dcyd-client-log-stderr')
    logger.setLevel(logging.INFO)
    logger.handle = lambda record: print(json.dumps(record.msg), file=sys.stderr)
    return logger


def get_gcp_logger() -> logging.Logger:
    '''
    Initialize a GCP logger.

    TODO: extra the client initialization logic
    '''
    key_file_path = request_service_account_key()
    if not key_file_path:
        utils.report_client_error('Unable to request service credentials. Data will not be be sent to DCYD.')
        return get_stderr_logger()

    client = google.cloud.logging.Client.from_service_account_json(key_file_path)

    handler = google.cloud.logging.handlers.handlers.CloudLoggingHandler(
        client=client,
        name='mpm-client-log',  # NOTE: This logger name is critical for downstream data processing. Do not change
        transport=gcl_patch.BackgroundThreadTransport,
    )
    handler.setFormatter(ExtractMsgFormatter())

    logger = logging.getLogger('mpm-client-log')
    logger.setLevel(logging.NOTSET)
    logger.addHandler(handler)
    return logger


def get_file_logger(*, log_file_path: str = os.getenv('DCYD_CLIENT_FILE_LOGGER')) -> logging.Logger:
    '''
    Initialize a file logger
    '''
    if not log_file_path:
        return None

    logger = logging.getLogger('dcyd-client-log-file')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file_path)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger

def get_http_logger(*, endpoint: str = os.getenv('DCYD_CLIENT_HTTP_LOGGER')) -> logging.Logger:
    '''
    Initialize an HTTP logger
    '''
    if not endpoint:
        return None
    logger = logging.getLogger('dcyd-client-log-http')
    logger.setLevel(logging.INFO)
    logger.handle = lambda record: requests.post(endpoint, json=record.msg)
    return logger


FILE_LOGGER = get_file_logger()
HTTP_LOGGER = get_http_logger()
GCP_LOGGER = get_gcp_logger()


def log_struct(record: dict):
    '''
    Write a dictionary to GCP Logging
    '''
    if FILE_LOGGER:
        FILE_LOGGER.info(json.dumps({
            'insertId': utils.generate_uid(),
            'jsonPayload': record,
            'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
            'receiveTimestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        }))
    if HTTP_LOGGER:
        HTTP_LOGGER.info({
            'insertId': utils.generate_uid(),
            'jsonPayload': record,
            'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
            'receiveTimestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        })
    return GCP_LOGGER.log(level=logging.INFO, msg=record)
