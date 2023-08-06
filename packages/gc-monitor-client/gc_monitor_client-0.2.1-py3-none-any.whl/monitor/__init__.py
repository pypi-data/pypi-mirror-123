import logging
from copy import deepcopy
from json import dumps
from os import environ
from time import time
from typing import Any
from typing import Dict
from typing import Optional

from assume_role import assume_role
from boto3.session import Session

LOGGER = logging.getLogger(__file__)


def create_session() -> Optional[Session]:
    role_arn = environ["MONITOR_ASSUME_ROLE_ARN"]
    if role_arn:
        return assume_role(arn=role_arn, session_name="deidentifier")
    return None


def calculate_default_attributes() -> Dict[str, str]:
    result: Dict[str, str] = dict()
    if attrs := environ["MONITOR_ATTRIBUTES"]:
        try:
            for attr in attrs.split(";"):
                attr_k, attr_v = attr.split("=", 1)
                result[attr_k] = attr_v
        except Exception:
            result["tags"] = dict(problem="could not decode MONITOR_ATTRIBUTES")  # type: ignore

    return result


SESSION = create_session()
DEFAULT_ATTRIBUTES = calculate_default_attributes()


def insert(**kwargs: str) -> None:
    if not SESSION:
        LOGGER.info("No monitor, not logging there.")
        return
    payload: Dict[str, Any] = deepcopy(DEFAULT_ATTRIBUTES)
    for attr in ["product", "service", "variant", "subtype", "activity"]:
        payload.setdefault(attr, "undefined")
        if attr in kwargs:
            payload[attr] = kwargs.pop(attr)
    payload["generation-epoch-time"] = int(time())
    kwargs.pop("password", None)  # just in case, shouldn't normally be one
    if kwargs:
        payload.setdefault("tags", dict())
        payload["tags"].update(kwargs)

    if "tags" in payload:
        # ensure they are strings
        payload["tags"] = {kw: str(val) for kw, val in payload["tags"].items()}

    LOGGER.info(f"Logging with {payload=}")
    lambda_client = SESSION.client("lambda", region_name=environ["MONITOR_REGION"])
    lambda_client.invoke(
        FunctionName=environ["MONITOR_LAMBDA_NAME"],
        InvocationType="Event",
        Payload=dumps(payload),
    )
