import enum
import re
from typing import Pattern, List


class ComplexSecretPattern:
    """ Inclusion and exclusions lists of regex to trigger a finding """
    inclusions: List[Pattern]
    exclusions: List[Pattern]

    def __init__(self, inclusions: List[Pattern], exclusions: List[Pattern]):
        self.inclusions = inclusions
        self.exclusions = exclusions


class SecretPattern(enum.Enum):
    """ Regexp for secret detection """
    CREDENTIAL_FILE = ComplexSecretPattern([re.compile(".*credentials.*")], [])
    AWS_KEY = ComplexSecretPattern(
        [re.compile(".*((A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Za-z0-9/+=]{16})")], [])
    AWS_SECRET = ComplexSecretPattern([re.compile(".*(?:AWS|aws).*([A-Za-z0-9/+=]{40})")], [
        re.compile('[a-f0-9]{64}'),
        re.compile('[a-f0-9]{96}'),
        re.compile('[a-f0-9]{128}'),
        re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    ])
    AZURE_CLIENT_ID = ComplexSecretPattern(
        [re.compile(".*(?:AZURE|azure).*(([0-9A-Fa-f]{8}-){1,}([0-9A-Fa-f]{4}-){3,}[0-9A-Fa-f]{12}).*")],
        [
            re.compile('[a-f0-9]{64}'),
            re.compile('[a-f0-9]{96}'),
            re.compile('[a-f0-9]{128}'),
            # re.compile('([0-9A-Fa-f]{8}-){1}([0-9A-Fa-f]{4}-){3}[0-9A-Fa-f]{12}'),
            re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]'
                       '|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        ])
    TWITTER_KEY = ComplexSecretPattern([re.compile(".*((?i)twitter(.{0,20})).*")], [])
    NPM_TOKEN = ComplexSecretPattern([re.compile(".*(?:NPM_KEY|npm_key|NPM_TOKEN|npm_token).*(([0-9A-Fa-f]{8}-){1,}"
                                                 "([0-9A-Fa-f]{4}-){3,}[0-9A-Fa-f]{12})")], [])
    GITHUB_KEY = ComplexSecretPattern([re.compile(".*((ghu|ghs|gho|ghp)_[0-9a-zA-Z]{36}).*")], [])
    GCP_KEY = ComplexSecretPattern([re.compile(".*((?i)AIza).*")], [])
    GCP_SERVICE_ACCOUNT = ComplexSecretPattern([re.compile(".*((?i)service_account).*")], [])
    HEROKU_KEY = ComplexSecretPattern([re.compile(".*((?i)heroku).*")], [])
    SHOPIFY_KEY = ComplexSecretPattern([re.compile(".*((?i)(shpss|shpat|shpca|shppa)_[a-fA-F0-9]{32}).*")], [])
    PIPY_KEY = ComplexSecretPattern([re.compile(".*((?i)(pypi-AgEIcHlwaS5vcmc)).*")], [])
    # //    FACEBOOK_KEY=.*(((?i)fb(.{0,20}))|((?i)facebook(.{0,20}))).*"
