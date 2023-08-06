# strledger - Sign Stellar Transaction with Ledger on the command line.

![example](https://github.com/overcat/strledger/blob/main/img/example.png)

## Installation
```shell
pip install -U strledger
```

## Usage
```text
Usage: strledger [OPTIONS] COMMAND [ARGS]...

  Stellar Ledger commands.

  This project is built on the basis of ledgerctl, you can check ledgerctl for more features.

Options:
  -v, --verbose  Display exchanged APDU.
  --help         Show this message and exit.

Commands:
  app-config   Get Stellar app config.
  get-address  Get Stellar public address.
  sign-tx      Sign a base64-encoded transaction envelope.
  version      Get version info.
```