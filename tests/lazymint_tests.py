import smartpy as sp
from ..contracts.lazymint import LazyMint


@sp.add_test(name="lazymint works fine trust me")
def test():
    scenario = sp.test_scenario()
    # test accounts
    admin = sp.test_account("admin")
    elon = sp.test_account("elon")
    pikachu = sp.test_account("pikachu")

    lazymint = LazyMint(
        admin=admin.address,
        contractAddress=sp.address("KT1LPSGeRj4FENhm9anHJUQy9epAwtttDwLh"),
    )
    scenario += lazymint
    message = sp.record(
        contractAddress=sp.address("KT1LPSGeRj4FENhm9anHJUQy9epAwtttDwLh"),
        tokenId=1,
        tokenOwner=admin.address,
        price=sp.mutez(69),
        tokenURI=sp.string("ipfs://dogetothemoon"),
    )
    digest = sp.pack(message)
    voucher = sp.record(
        message=message,
        signature=sp.make_signature(admin.secret_key, digest, message_format="Raw"),
        publickey=admin.public_key,
    )
    scenario += lazymint.redeem(redeemer=elon.address, voucher=voucher).run(
        sender=elon.address, amount=message.price
    )
    scenario.show(lazymint.balance)
    # validates the voucher is invalidated
    scenario.verify(lazymint.data.invalidated_voucher[digest] == sp.bool(True))
    ## invalid tests
    # token already minted error
    scenario += lazymint.redeem(redeemer=elon.address, voucher=voucher).run(
        sender=elon.address, amount=message.price, valid=False
    )

    # invalid amount error
    message = sp.record(
        contractAddress=sp.address("KT1LPSGeRj4FENhm9anHJUQy9epAwtttDwLh"),
        tokenId=2,
        tokenOwner=admin.address,
        price=sp.mutez(69),
        tokenURI=sp.string("ipfs://abkibaarmodisarkar"),
    )
    digest = sp.pack(message)
    voucher = sp.record(
        message=message,
        signature=sp.make_signature(admin.secret_key, digest, message_format="Raw"),
        publickey=admin.public_key,
    )
    scenario += lazymint.redeem(redeemer=elon.address, voucher=voucher).run(
        sender=elon.address, amount=sp.mutez(420), valid=False
    )
    # invalid signature error
    message = sp.record(
        contractAddress=sp.address("KT1LPSGeRj4FENhm9anHJUQy9epAwtttDwLh"),
        tokenId=3,
        tokenOwner=admin.address,
        price=sp.mutez(69),
        tokenURI=sp.string("ipfs://tezbetterthaneth"),
    )
    digest = sp.pack(message)
    voucher = sp.record(
        message=message,
        signature=sp.make_signature(admin.secret_key, digest, message_format="Raw"),
        publickey=elon.public_key,
    )
    scenario += lazymint.redeem(redeemer=elon.address, voucher=voucher).run(
        sender=elon.address, amount=sp.mutez(420), valid=False
    )
    # invalid sender
    message = sp.record(
        contractAddress=sp.address("KT1LPSGeRj4FENhm9anHJUQy9epAwtttDwLh"),
        tokenId=4,
        tokenOwner=admin.address,
        price=sp.mutez(69),
        tokenURI=sp.string("ipfs://iamdonebeingfunny"),
    )
    digest = sp.pack(message)
    voucher = sp.record(
        message=message,
        signature=sp.make_signature(admin.secret_key, digest, message_format="Raw"),
        publickey=admin.public_key,
    )
    scenario += lazymint.redeem(redeemer=elon.address, voucher=voucher).run(
        sender=pikachu.address, amount=sp.mutez(420), valid=False
    )
