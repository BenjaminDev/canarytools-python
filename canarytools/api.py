# Design: Is this a solid way to track api endpoints and potential changes?
# Let's see where things hit the ground
from typing import Dict, Tuple

base_url = f"https://{{}}.canary.tools"
api_version = "v1"

api_endpoints: Dict[Tuple[str, str], str] = dict()
# REF: https://docs.canary.tools/console-settings/overview.html#overview
api_endpoints[("get", "settings")] = "/settings"
api_endpoints[("post", "settings_api_disable")] = "/settings/api/disable"
api_endpoints[("post", "settings_api_enable")] = "/settings/api/enable"
api_endpoints[("get", "settings_api_auth_token_download")] = "/token/download"

# REF: https://docs.canary.tools/incidents/actions.html#actions
api_endpoints[("post", "incident_acknowledge")] = "/incident/acknowledge"
api_endpoints[("delete", "incident_delete")] = "/incident/delete"
api_endpoints[("get", "incident_fetch")] = "/incident/fetch"
api_endpoints[("post", "incident_unacknowledge")] = "/incident/unacknowledge"

api_endpoints[("post", "incidents_unacknowledge")] = "/incidents/unacknowledge"
api_endpoints[("delete", "incidents_delete")] = "/incidents/delete"
api_endpoints[("post", "incidents_acknowledge")] = "/incidents/acknowledge"

# REF: https://docs.canary.tools/incidents/queries.html#queries
api_endpoints[("get", "incident_acknowledged")] = "/incidents/acknowledged"
api_endpoints[("get", "incident_unacknowledged")] = "/incidents/unacknowledged"
api_endpoints[("get", "incident_all")] = "/incidents/all"


# REF: https://docs.canary.tools/bird-management/queries.html#bird-info
api_endpoints[("get", "devices_all")] = "/devices/all"
api_endpoints[("get", "devices_live")] = "/devices/live"
api_endpoints[("get", "devices_dead")] = "/devices/dead"
api_endpoints[("get", "devices_filter")] = "/devices/filter"
api_endpoints[("get", "device_info")] = "/device/info"
api_endpoints[("get", "device_ips")] = "/device/ips"

# REF: https://docs.canary.tools/flocks/queries.html#queries
api_endpoints[("get", "flock_list")] = "/flock/list"
api_endpoints[("get", "flock_settings")] = "/flock/settings"
api_endpoints[("get", "flock_summary")] = "/flock/summary"
api_endpoints[("get", "flock_users")] = "/flock/users"
api_endpoints[("get", "flocks_filter")] = "/flocks/filter"
api_endpoints[("get", "flocks_list")] = "/flocks/list"
api_endpoints[("get", "flocks_summary")] = "/flocks/summary"

# REF: https://docs.canary.tools/flocks/notes.html#notes
api_endpoints[("get", "flock_note")] = "/flock/note"
api_endpoints[("post", "flock_note")] = "/flock/note/add"
api_endpoints[("delete", "flock_note")] = "/flock/note/delete"
# GET
# /api/v1/flock/note
# POST
# /api/v1/flock/note/add
# DELETE
# /api/v1/flock/note/delete
