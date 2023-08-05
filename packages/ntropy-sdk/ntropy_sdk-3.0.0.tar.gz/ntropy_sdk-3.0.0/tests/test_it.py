from unittest import TestCase

from ntropy_sdk import SDK, Transaction


class TxTest(TestCase):
    def test_enrich(self):
        api_key = "R6yiREz91PfXPjIfsjHqpVE4VGgjATXVjGrxuv3H"
        sdk = SDK(api_key)
        sdk.base_url = "http://staging.ntropy.network"

        tx = Transaction(
            amount=24.56,
            description="coin car wash",
            entry_type="debit",
            country="US",
            date="2012-12-10",
            account_holder_id="1",
        )

        resp = sdk.enrich(tx)

        print("HELLO")
        print(resp)

        resp = sdk.enrich(tx, latency_optimized=True)
        print(resp)

        txs = [tx, tx, tx]

        resp = sdk.enrich_batch(txs, categorization=False)

        print(resp)

        result = resp.wait()

        print(result.transactions)
