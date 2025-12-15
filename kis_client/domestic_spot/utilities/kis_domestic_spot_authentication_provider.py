import hashlib
import hmac


class KoreaInvestmentSecuritiesDomesticSpotAuthenticationProvider:
    @staticmethod
    def create_authentication_signature(query_string: str, private_key: str) -> str:
        signature = hmac.new(private_key.encode("utf-8"),
                             query_string.encode("utf-8"),
                             hashlib.sha256).hexdigest()
        return signature
