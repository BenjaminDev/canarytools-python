import dataclasses
import json
from typing import Any, List, Optional

from pydantic import BaseModel, Field, FilePath

from .base import AuthToken


class AuthFile(BaseModel):
    auth_token_file_as_bytes: bytes
    auth_token_file: Optional[FilePath]


class ThinkstResult(BaseModel):
    result: str


class Settings(BaseModel):
    auth_token: AuthToken
    auth_token_enabled: bool
    canarytokens_user_domains_enable: bool
    canarytokens_webroot_enable: bool
    console_domain: str
    # TODO: what is console_settings_change_enable
    console_settings_change_enable: bool
    device_settings_change_enable: bool
    email_notification_enable: bool
    generic_incident_webhooks: List[str]
    globally_enforce_2fa: bool
    hipchat_integration_urls: List[str]

    def __init__(__pydantic_self__, **data: Any) -> None:
        # if isinstance(data_as_str, str):
        # data_as_str=None,
        #     data = json.loads(data_as_str)
        # breakpoint()
        data["auth_token"] = AuthToken(auth_token=data["auth_token"])
        super().__init__(**data)


#   "incident_webhooks_enabled": true,
#   "module_options": {
#     "canarytokens_public_ip": "<ip_address>",
#     "canarytokens_user_domains": "",
#     "canarytokens_webroot": "<html><body>example!</body></html>",
#     "canaryvm_remaining_licenses": 10,
#     "canaryvm_version_details": [
#       {
#         "commit": "8a06e02",
#         "link": "<download_link>",
#         "ovalink": "<ova_link>",
#         "password": "<password>",
#         "seedlink": "<seed_link>",
#         "version": "2.2.1"
#       }
#     ],
#     "saml_enabled": false,
#     "ssh_credential_watch_only": null,
#     "ssh_credential_watches": "",
#     "ssh_credential_watches_enable": null,
#     "update_automatically_enable": true
#   },
#   "ms_teams_webhooks": [],
#   "notification_addresses": [
#     "<email_address>"
#   ],
#   "notification_numbers": [
#     "<cellphone_number>"
#   ],
#   "result": "success",
#   "sensitive_data_masking_enable": false,
#   "slack_incident_webhook": [],
#   "sms_notification_enable": false,
#   "summary_email_addresses": [
#     "<email_address>"
#   ],
#   "summary_email_enable": false,
#   "syslog_enabled": false,
#   "syslog_facility": "local0",
#   "syslog_hostname": "localhost",
#   "syslog_loglevel": "crit",
#   "syslog_port": "514",
#   "syslog_protocol": "tcp",
#   "syslog_tls": "off",
#   "whitelist_enable": true,
#   "whitelist_hostnames": "<hostname>",
#   "whitelist_hostnames_enable": true,
#   "whitelist_ips": "<ip_address>,<ip_address>",
#   "whitelist_oid_enable": false,
#   "whitelist_oids": "",
#   "whitelist_src_port_enable": true,
#   "whitelist_src_port_ips": "<ip_address>:<port>"
# }
