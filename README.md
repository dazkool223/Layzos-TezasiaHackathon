# Layzos - Future For Gas-free Minting
>First implemention of a smart contract that supports lazymint on Tezos

## Overview
Due to lazy minting, it's possible to defer the cost of minting an NFT until the moment it's sold to its first buyer. The gas fees for minting are rolled into the same transaction that assigns the NFT to the buyer, so the NFT creator never has to pay to mint. Instead, a portion of the purchase price simply goes to cover the additional gas needed to create the initial NFT record. The basic premise of lazy minting is that instead of creating an NFT directly by calling a contract function, the NFT creator prepares a *cryptographic signature* of some data using their Tezos account's private key. The signed data acts as a "voucher" that can be redeemed for an NFT. The voucher contains all the information that will go into the actual NFT, and it may optionally contain additional data that isn't recorded in the blockchain. The signature proves that the NFT creator authorised the creation of the specific NFT described in the voucher.

## Inspiration
Since writing data onto the blockchain requires fees to pay for the computation and storage. 
This can be a barrier for NFT creators, especially those new to NFTs who may not want to invest a lot of money upfront before knowing whether their work will sell. This will be helpful small-time NFT creators who are unable to bear the cost of minting but are willing to showcase their work on blockchain.
Since, Huge NFT platforms like OpenSea supports the feature of lazyminting on ethereum, we are the first ones to devise such functionality inside the tezos blockchain

## How will it help in growing the existing Tezos ecosystem?
- More people are encouraged to mint NFTs of tezos blockchain due to no cost at the minting level.
- Currently, this feature is available on a few blockchains like Ethereum.
- Lazy minting fosters liquidity since NFTs can only be transferred after being sold. This helps prevent sellers from being left with a collection of minted, unsold NFTs, and buyers aren’t left waiting indefinitely for the NFT to be transferred to them.

## Contracts
There are two contracts made to implement the lazyminting process. One is custom-made to handle the [FA2 token](contracts/fa2.py) transactions and other is to [lazymint](contracts/lazymint.py) i.e validate the voucher and mint the corresponding NFT according to the data mentioned in the voucher. Sample Parameters are available [here](tests)

## Future Scopes
- Validation of chain_ids to further enhance the security of the vouchers so that a voucher made on a testnet cannot be redeemed on the mainnet.
- Addition of Minting Roles
- Implementing Collections and Royalties to the token owner during each transaction of the NFT.
## 
#### [FA2 Contract](https://better-call.dev/jakartanet/KT1XkZjMpL5R2aZ5PWTrn1e6tzfBRLAxSdkD/)
#### [LazyMint Contract](https://better-call.dev/jakartanet/KT1SiBT7p6SZM64LBPJZN5GFYQbxUpMXQuQH)
#### [Video Demo](https://drive.google.com/file/d/1UThdol3o9yYTmX3zv5EiQWI68XSg9h44/view?usp=drivesdk)
### References
- [What is Cryptographic Signature ?](https://docs.microsoft.com/en-us/dotnet/standard/security/cryptographic-signatures)
- [Understanding NFT Storages](https://nft.storage/docs/)
- [Understanding IPFS](https://docs.ipfs.tech/concepts/how-ipfs-works/)
- [Understanding FA2 Standard](https://tzip.tezosagora.org/proposal/tzip-12/)
- [Implementation information in ETH](https://github.com/yusefnapora/lazy-minting)

#### Special thanks to [Anshu Jalan](https://github.com/AnshuJalan) for helping us throughout the implementation process!
