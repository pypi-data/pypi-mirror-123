import sys
from argparse import Namespace

from dstack.cli import get_or_ask
from dstack.cli.common import do_post, sensitive
from dstack.config import ConfigurationError


def config_func(args: Namespace):
    aws_access_key_id = get_or_ask(args, None, "aws_access_key_id", "AWS Access Key ID: ", secure=True)
    aws_secret_access_key = get_or_ask(args, None, "aws_secret_access_key", "AWS Secret Access Key: ", secure=True)
    aws_region = get_or_ask(args, None, "aws_region", "Region name: ", secure=False)
    try:
        data = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "aws_region": aws_region,
        }
        response = do_post("users/aws/config", data)
        if response.status_code == 200:
            print("Succeeded")
        if response.status_code == 400 and response.json().get("message") == "non-cancelled requests":
            sys.exit(f"Call 'dstack rules clear' first")
        else:
            response.raise_for_status()
    except ConfigurationError:
        sys.exit(f"Call 'dstack login' or 'dstack register' first")


def info_func(_: Namespace):
    try:
        response = do_post("users/aws/info")
        if response.status_code == 200:
            response_json = response.json()
            print("aws_access_key_id: " + (sensitive(response_json.get("aws_access_key_id")) or "no"))
            print("aws_secret_access_key: " + (sensitive(response_json.get("aws_secret_access_key")) or "no"))
            print("aws_region: " + (response_json.get("aws_region") or "no"))
        else:
            response.raise_for_status()
    except ConfigurationError:
        sys.exit(f"Call 'dstack login' or 'dstack register' first")


def clear_func(_: Namespace):
    try:
        response = do_post("users/aws/clear")
        if response.status_code == 200:
            print("Succeeded")
        elif response.status_code == 400 and response.json().get("message") == "non-cancelled requests":
            sys.exit(f"Call 'dstack rules clear' first")
        else:
            response.raise_for_status()
    except ConfigurationError:
        sys.exit(f"Call 'dstack login' or 'dstack register' first")


def register_parsers(main_subparsers):
    parser = main_subparsers.add_parser("aws", help="Manage own AWS cloud configuration")

    subparsers = parser.add_subparsers()

    configure_parser = subparsers.add_parser("configure", help="Specify own AWS cloud credentials")
    configure_parser.add_argument("--aws-access-key-id", type=str, dest="aws_access_key_id")
    configure_parser.add_argument("--aws-secret-access-key", type=str, dest="aws_secret_access_key")
    configure_parser.add_argument("--aws-region", type=str, dest="aws_region")
    configure_parser.set_defaults(func=config_func)

    info_parser = subparsers.add_parser("info", help="Display the current configuration")
    info_parser.set_defaults(func=info_func)

    clear_parser = subparsers.add_parser("clear", help="Clear the current configuration")
    clear_parser.set_defaults(func=clear_func)

