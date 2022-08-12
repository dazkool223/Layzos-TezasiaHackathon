"""
This is the customised FA2 contract having two functions
1. mint():
it verifies admin with few other conditions and mints tokens by updating 
the ledger, supply mapping, counters and token metadata according the requirements of the lazyminting

2. transfer():
function for performing the transfer operation from the tokenOwner to the buyer.

these both functions are called in the redeem() function in the lazymint contract
"""

import smartpy as sp

FA2 = sp.io.import_template("FA2.py")


class Types:
    VOUCHER = sp.TRecord(
        contractAddress=sp.TAddress,
        tokenId=sp.TNat,
        tokenOwner=sp.TAddress,
        price=sp.TMutez,
        tokenURI=sp.TString,
    )

    LEDGER_KEY = sp.TPair(
        # tokenOwner
        sp.TAddress,
        # tokenId
        sp.TNat,
    )

    TRANSFER = sp.TList(
        sp.TRecord(
            from_=sp.TAddress,
            txs=sp.TList(sp.TRecord(to_=sp.TAddress, token_id=sp.TNat, amount=sp.TNat)),
        )
    )

    OPERATOR_KEY = sp.TRecord(
        # The owner of the token editions
        owner=sp.TAddress,
        # The operator allowed by the owner to transfer their token editions
        operator=sp.TAddress,
        # The token id
        token_id=sp.TNat,
    )


class Token(sp.Contract):
    def __init__(self, administrator):
        # type setting of class
        self.init_type(
            sp.TRecord(
                # address of admin
                administrator=sp.TAddress,
                # ledger where tokenOwners are listed
                ledger=sp.TBigMap(Types.LEDGER_KEY, sp.TNat),
                # counter that keeps track of total minted tokens
                counter=sp.TNat,
                # to keep track of total supply
                supply=sp.TBigMap(sp.TNat, sp.TNat),
                # stores the ipfs metadata link along with the token id
                token_metadata=sp.TBigMap(sp.TNat, sp.TString),
                # token_id field of fa2
                token_id=sp.TNat,
                # voucher which will be sent by the lazymint
                operators=sp.TBigMap(Types.OPERATOR_KEY, sp.TUnit),
            )
        )
        self.init(
            administrator=administrator,
            ledger=sp.big_map(),
            counter=sp.nat(0),
            supply=sp.big_map(),
            token_metadata=sp.big_map(),
            token_id=sp.nat(0),
            operators=sp.big_map(),
        )

    def check_is_administrator(self):
        sp.verify(sp.sender == self.data.administrator, message="FA2_NOT_ADMIN")

    def check_token_exists(self, token_id):
        sp.verify(token_id < self.data.counter, message="FA2_TOKEN_UNDEFINED")

    @sp.entry_point
    def mint(self, params):
        sp.set_type(params, Types.VOUCHER)
        self.check_is_administrator()

        # updating the values in storage

        token_id = sp.compute(self.data.counter)

        self.data.ledger[(params.tokenOwner, token_id)] = sp.utils.mutez_to_nat(
            params.price
        )

        self.data.supply[token_id] = sp.utils.mutez_to_nat(params.price)

        self.data.token_metadata[token_id] = params.tokenURI

        self.data.counter += 1

    @sp.entry_point
    def transfer(self, params):
        sp.set_type(params, Types.TRANSFER)

        with sp.for_("transfer", params) as transfer:
            with sp.for_("tx", transfer.txs) as tx:
                # Check that the token exists
                token_id = sp.compute(tx.token_id)
                self.check_token_exists(token_id)

                # Check that the sender is one of the token operators
                owner = sp.compute(transfer.from_)
                sp.verify(
                    (sp.sender == owner)
                    | self.data.operators.contains(
                        sp.record(owner=owner, operator=sp.sender, token_id=token_id)
                    ),
                    message="FA2 OPERATOR ERROR",
                )

                # Check that the transfer amount is not zero
                with sp.if_(tx.amount > 0):
                    # Remove the token amount from the owner
                    owner_key = sp.pair(owner, token_id)
                    self.data.ledger[owner_key] = sp.as_nat(
                        self.data.ledger.get(owner_key, 0) - tx.amount,
                        "FA2_INSUFFICIENT_BALANCE",
                    )

                    # Add the token amount to the new owner
                    new_owner_key = sp.pair(tx.to_, token_id)
                    self.data.ledger[new_owner_key] = (
                        self.data.ledger.get(new_owner_key, 0) + tx.amount
                    )
