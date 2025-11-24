import logging
import os

import requests.adapters
from exchangelib import Account
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


def list_items(account: Account) -> None:
    for item in account.inbox.all().order_by("-datetime_received")[:3]:
        print(item.subject, item.sender, item.datetime_received)


def main():
    # show_logs()
    clear_cache()
    validate_custom_certificate()
    credentials = provide_credentials()
    account = sign_into_account_using_autodiscover(credentials)
    list_items(account)


if __name__ == "__main__":
    main()
