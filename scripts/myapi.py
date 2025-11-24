import logging
import os
import shelve

import requests.adapters
from exchangelib import DELEGATE
from exchangelib import Account
from exchangelib import Configuration
from exchangelib import Credentials
from exchangelib.autodiscover import clear_cache
from exchangelib.protocol import BaseProtocol
from exchangelib.util import PrettyXmlHandler


class RootCAAdapter(requests.adapters.HTTPAdapter):
    def cert_verify(self, conn, url, verify, cert):
        super().cert_verify(
            conn=conn,
            url=url,
            verify=os.getenv("CERTIFICATE_PATH"),
            cert=cert,
        )


def show_logs() -> None:
    logging.basicConfig(level=logging.DEBUG, handlers=[PrettyXmlHandler()])


def validate_custom_certificate() -> None:
    BaseProtocol.HTTP_ADAPTER_CLS = RootCAAdapter


def provide_credentials() -> Credentials:
    return Credentials(
        username=os.getenv("CREDENTIALS_USERNAME"),
        password=os.getenv("CREDENTIALS_PASSWORD"),
    )


def sign_into_account_using_autodiscover(credentials: Credentials) -> Account:
    return Account(
        primary_smtp_address=os.getenv("PRIMARY_SMTP_ADDRESS"),
        credentials=credentials,
        autodiscover=True,
    )


def sign_into_account_using_configuration_object(credentials: Credentials) -> Account:
    with shelve.open(os.getenv("CACHE_PATH")) as cache:
        config = Configuration(
            service_endpoint=cache["ews_url"],
            credentials=credentials,
            auth_type=cache["ews_auth_type"],
            version=cache["version"],
        )
        return Account(
            primary_smtp_address=cache["primary_smtp_address"],
            config=config,
            autodiscover=False,
            access_type=DELEGATE,
        )


def cache_autodiscover_results(account: Account) -> None:
    with shelve.open(os.getenv("CACHE_PATH")) as cache:
        cache["ews_url"] = account.protocol.service_endpoint
        cache["ews_auth_type"] = account.protocol.auth_type
        cache["primary_smtp_address"] = account.primary_smtp_address
        cache["version"] = account.version


def list_items(account: Account) -> None:
    for item in account.inbox.all().order_by("-datetime_received")[:3]:
        print(item.subject, item.sender, item.datetime_received)


def sign_into_account():
    validate_custom_certificate()
    credentials = provide_credentials()
    return sign_into_account_using_configuration_object(credentials)


def main():
    # show_logs()
    clear_cache()
    validate_custom_certificate()
    credentials = provide_credentials()
    # account = sign_into_account_using_autodiscover(credentials)
    # cache_autodiscover_results(account)
    account = sign_into_account_using_configuration_object(credentials)
    list_items(account)


if __name__ == "__main__":
    main()
