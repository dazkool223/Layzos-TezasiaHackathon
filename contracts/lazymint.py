"""
This is the Lazymint contract in with redeem() function

A 'voucher' with suitable parameters (i.e. fields required for minting, signature, publickey of the owner)
are sent to the redeem() along with the redeemers address
then the function :
1. verifies the signature that the message is actually signed by the tokenOwner.
2. mints the token with appropriate data fields with the fa2.mint() on the address of the tokenOwner.
3. transfers the token from the tokenOwner to redeemer with the fa2.mint().
4. invalidates the voucher so that it is not used again.

this function is called by the redeemer.
"""
import smartpy as sp

# class for type setting of records
class Types:
    MESSAGE = sp.TRecord(
        contractAddress=sp.TAddress,
        tokenId=sp.TNat,
        tokenOwner=sp.TAddress,
        price=sp.TMutez,
        tokenURI=sp.TString,
    )
    VOUCHER = sp.TRecord(
        message=MESSAGE,
        signature=sp.TSignature,
        publickey=sp.TKey,
    )
    TRANSFER = sp.TRecord(
        from_=sp.TAddress,
        txs=sp.TRecord(to_=sp.TAddress, token_id=sp.TNat, amount=sp.TNat),
    )


# class for performing lazyminting operations


class LazyMint(sp.Contract):
    def __init__(
        self,
        admin,
        contractAddress,
        counter=sp.nat(0),
        invalidated_voucher=sp.big_map(),
    ):

        self.init_type(
            sp.TRecord(
                # admin for initialise the contract
                admin=sp.TAddress,
                # bigmap to maintain record of minted tokens
                counter=sp.TNat,
                contractAddress=sp.TAddress,
                invalidated_voucher=sp.TBigMap(sp.TBytes, sp.TBool),
            )
        )

        # initialise the storage
        self.init(
            admin=admin,
            contractAddress=sp.address("KT1LPSGeRj4FENhm9anHJUQy9epAwtttDwLh"),
            counter=0,
            invalidated_voucher=sp.big_map(),
        )

    # signature verification function
    def verify_signature(self, voucher):
        sp.set_type(voucher, Types.VOUCHER)

        # creates a replica digest in the format of the request sent from the frontend
        digest = sp.pack(voucher.message)

        # uses the check_signature with the tokenOwner and the digest
        isValid = sp.check_signature(voucher.publickey, voucher.signature, digest)
        sp.verify(isValid, "INVALID SIGNATURE")

    @sp.entry_point
    def redeem(self, redeemer, voucher):
        # type setting of each parameter
        sp.set_type(redeemer, sp.TAddress)
        sp.set_type(voucher, Types.VOUCHER)

        message = voucher.message
        # verify the signature with the digest and the signature
        self.verify_signature(voucher)
        # condition to check the if redeem is called by the redeemer
        sp.verify(sp.sender == redeemer, "INVALID SENDER")
        # check whether buyer has sent enough tez to buy the nft
        sp.verify(sp.amount == message.price, "INVALID AMOUNT")
        # check the token is already minted or not
        sp.verify(voucher.message.tokenId > self.data.counter, "TOKEN ALREADY MINTED")
        # check the voucher is valid
        digest = sp.pack(voucher.message)
        sp.verify(~self.data.invalidated_voucher.contains(digest), "INVALID VOUCHER")
        # mint the token to the tokenOwner using the data present in the voucher
        fa2mint = sp.contract(
            Types.MESSAGE, self.data.contractAddress, entry_point="mint"
        ).open_some()

        sp.transfer(
            arg=sp.record(
                contractAddress=message.contractAddress,
                tokenId=message.tokenId,
                tokenOwner=message.tokenOwner,
                price=message.price,
                tokenURI=message.tokenURI,
            ),
            amount=sp.mutez(0),
            destination=fa2mint,
        )
        # increase the counter
        self.data.counter += 1
        # transfer the tokens from the tokenOwner to the redeemer
        fa2transfer = sp.contract(
            Types.TRANSFER,
            address=self.data.contractAddress,
            entry_point="transfer",
        ).open_some()

        sp.transfer(
            arg=sp.record(
                from_=message.tokenOwner,
                txs=sp.record(to_=redeemer, token_id=message.tokenId, amount=sp.nat(1)),
            ),
            amount=sp.mutez(0),
            destination=fa2transfer,
        )
        # sending tez to the tokenOwner
        sp.send(message.tokenOwner, sp.amount, message="COULD NOT SEND")
        # Invalidate the voucher to further prevent it to mint on the other marketplaces
        digest = sp.pack(voucher.message)
        self.data.invalidated_voucher[digest] = sp.bool(True)

