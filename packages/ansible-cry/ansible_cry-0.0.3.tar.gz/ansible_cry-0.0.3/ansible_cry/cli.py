#!/usr/bin/env python3
import re
import sys

from plumbum import cli
from ansible.parsing.vault import VaultLib, VaultSecret


class CRY(cli.Application):
    DESCRIPTION = "CRY me a river of encrypted data. Cry cry Cry."
    decrypt = cli.Flag(["-d", "--decrypt"], default=False,
                       help="Encrypt by default, add -d to decrypt")

    def main(self):
        if not self.nested_command:
            print("No command given")
            return 1  # error exit code
        with open('vault.pass', 'r') as pass_file:
            self.v = VaultLib([(None, VaultSecret(pass_file.read().encode()))])


@CRY.subcommand("file")
class CRYFile(cli.Application):

    @cli.positional(cli.ExistingFile)
    def main(self, *files):
        for file in files:
            with open(file, 'r') as f:
                file_in_str = f.read()
            if self.parent.decrypt:
                print(decrypt(file_in_str, self.parent.v))
            else:
                print(encrypt(file_in_str, self.parent.v))


@CRY.subcommand("string")
class CRYString(cli.Application):
    stdin = cli.Flag(["-s", "--stdin"], default=False,
                     help="Use stdin as source")

    def main(self, *strings):

        if self.stdin:
            strings = [sys.stdin.read()]

        if self.parent.decrypt:
            for s in strings:
                print(decrypt(s, self.parent.v))
        else:
            for s in strings:
                print(encrypt(s, self.parent.v))


def decrypt(s: str, v: VaultLib) -> str:
    decrypted_string = ""
    s += '\n\n'
    regex = r"\$ANSIBLE_VAULT;[0-9.]+;[A-Z0-9]+\n([0-9\sa-z])+^"
    matches = re.finditer(regex, s, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        m = match.group()
        if m:
            m = m.strip().replace(' ', '').replace('\t', '')
            print(v.decrypt(m).decode())
    return decrypted_string


def encrypt(s: str, v: VaultLib) -> str:
    return v.encrypt(s).decode()


if __name__ == "__main__":
    CRY.run()
