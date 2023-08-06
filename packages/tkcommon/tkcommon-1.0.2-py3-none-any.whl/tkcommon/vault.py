from os import getenv
import hvac
from .logger import get_logger


def _get_client(vault_url=None, vault_token=None):
    logger = get_logger(__name__)
    vault_url = getenv("VAULT_URL", vault_url)
    vault_token = getenv("VAULT_TOKEN", vault_token)
    if not vault_url:
        logger.error(
            "vault_url argument is not provided and VAULT_URL is not present in the environment"
        )
        return None
    if not api_key:
        logger.error(
            "vault_token argument is not provided and VAULT_TOKEN is not present in the environment"
        )
        return None
    client = hvac.Client(url=vault_url, token=vault_token)
    if client.is_authenticated():
        return client
    return None


def get_vault_secrets(path="", vault_url=None, vault_token=None):
    """get vault secrets for the path

    :param path: vault secrets path
    :type path: str
    :param vault_url: vault server url. If vault_url is none, VAULT_URL environment value will be assigned.
    :type vault_url: str
    :param vault_token: vault user access token. If vault_token is none, VAULT_TOKEN environment value will be assigned.
    :type vault_token: str
    :return: List(Dict[str, Any]) if successful, `None` otherwise
    """
    logger = get_logger(__name__)
    client = _get_client(vault_url=vault_url, vault_token=vault_token)
    if client is None:
        return None
    try:
        secrets = client.read(path)
        if "data" in secrets:
            secrets["data"]
    except Exception as e:
        logger.error(f"Got an error: {e.message}")
        return None
    return None
