import smartpy as sp
from ..contracts.fa2 import Token


@sp.add_test(name="mint")
def test():
    scenario = sp.test_scenario()
    # sample accounts
    admin = sp.test_account("admin")
    # admin address = tz1UyQDepgtUBnWjyzzonqeDwaiWoQzRKSP5
    musk = sp.test_account("user1")
    elon = sp.test_account("user2")
    # elon address = tz1KouJrf2JFUx8y15pZv7B36dtYQ3GcgJu3
    # instace of token class
    token = Token(administrator=admin.address)
    scenario += token
    sampleToken0 = sp.record(
        contractAddress=sp.address("KT1"),
        tokenId=sp.nat(0),
        tokenOwner=admin.address,
        price=sp.mutez(69),
        tokenURI=sp.string("ipfs://icandowhateveriwant"),
    )
    # token minted by admin
    scenario += token.mint(sampleToken0).run(sender=admin)

    sampleToken1 = sp.record(
        contractAddress=sp.address("KT1"),
        tokenId=sp.nat(0),
        tokenOwner=admin.address,
        price=sp.mutez(69),
        tokenURI=sp.string("ipfs://icantdoanythingevenifiamelon"),
    )
    # token minted by elon (not admin)
    scenario += token.mint(sampleToken1).run(sender=elon, valid=False)

    # sending invalid token
    tokentobetransfered1 = [
        sp.record(
            from_=admin.address,
            txs=[sp.record(to_=elon.address, token_id=69, amount=69)],
        )
    ]
    scenario += token.transfer(tokentobetransfered1).run(sender=admin, valid=False)

    # sending token with incorrect owner
    tokentobetransfered2 = [
        sp.record(
            from_=musk.address, txs=[sp.record(to_=elon.address, token_id=0, amount=69)]
        )
    ]
    scenario += token.transfer(tokentobetransfered2).run(sender=admin, valid=False)

    # sending invalid amount
    tokentobetransfered3 = [
        sp.record(
            from_=admin.address, txs=[sp.record(to_=elon.address, token_id=0, amount=1)]
        )
    ]
    scenario += token.transfer(tokentobetransfered3).run(sender=admin)

    # admin transfers token to elon without any error
    tt = [
        sp.record(
            from_=admin.address, txs=[sp.record(to_=elon.address, token_id=0, amount=1)]
        )
    ]
    scenario += token.transfer(tt).run(sender=admin)
