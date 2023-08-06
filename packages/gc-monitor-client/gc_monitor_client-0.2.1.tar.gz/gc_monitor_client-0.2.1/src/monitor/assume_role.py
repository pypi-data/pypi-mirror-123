import logging
import os
import pickle
import types
from functools import wraps
from hashlib import sha1
from os import environ
from time import time
from typing import Any
from typing import Callable
from typing import cast
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import TypeVar

import boto3
from boto3.session import Session

LOGGER = logging.getLogger(__file__)

F = TypeVar("F", bound=Callable[..., Any])


def cache(
    *, seconds: int, version: str = os.environ.get("DEPLOYMENT_ID", "1")
) -> Callable[[F], F]:
    store: Dict[bytes, Tuple[int, bytes]] = dict()

    def dec(f: F) -> F:
        @wraps(f)
        def x(__refreshhit: bool = False, **kw: Any) -> Any:
            now = int(time())
            fn_key = sha1(
                "cache-{} {} {}-{}".format(
                    f.__module__, f.__name__, sorted(kw.items()), version
                ).encode("utf-8")
            ).digest()
            expiry_time, cached_result = store.get(fn_key, (0, b""))
            if now <= expiry_time and not __refreshhit:
                return pickle.loads(cached_result)
            calculated_result = f(**kw)
            if calculated_result is None:
                LOGGER.warning("result will not be cached, as it is None")
            assert not isinstance(calculated_result, types.GeneratorType)
            store[fn_key] = (now + seconds, pickle.dumps(calculated_result))
            return calculated_result

        return cast(F, x)

    return dec


def assume_role(
    arn: str,
    session_name: str = "horizon",
    region_name: Optional[str] = None,
) -> Session:
    LOGGER.info(f"Assuming {arn}")
    return Session(
        **retrieve_assume_role_creds(
            arn=arn,
            session_name=session_name,
            region_name=region_name
            or environ.get("AWS_DEFAULT_REGION")
            or "unknown AWS region",
        )
    )


@cache(seconds=300)
def retrieve_assume_role_creds(
    arn: str,
    region_name: str,
    session_name: str = "horizon",
) -> Dict[str, str]:

    client = boto3.client("sts", region_name=region_name)
    response = client.assume_role(RoleArn=arn, RoleSessionName=session_name)
    return dict(
        aws_access_key_id=response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
        aws_session_token=response["Credentials"]["SessionToken"],
    )
