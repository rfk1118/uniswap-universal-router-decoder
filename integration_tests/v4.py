import os
import subprocess
import time

from eth_account.account import LocalAccount
from web3 import (
    Account,
    Web3,
)
from web3.types import Wei

from uniswap_universal_router_decoder import (
    FunctionRecipient,
    RouterCodec,
    V4Constants,
)


web3_provider = os.environ['WEB3_HTTP_PROVIDER_URL_ETHEREUM_MAINNET']
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

account: LocalAccount = Account.from_key("0xf7e96bcf6b5223c240ec308d8374ff01a753b00743b3a0127791f37f00c56514")
assert account.address == "0x1e46c294f20bC7C27D93a9b5f45039751D8BCc3e"

chain_id = 1
initial_block_number = 21839494

# Tokens
eth_address = Web3.to_checksum_address("0x0000000000000000000000000000000000000000")

weth_address = Web3.to_checksum_address("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
weth_abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]'  # noqa
weth_contract = w3.eth.contract(address=weth_address, abi=weth_abi)

wbtc_address = Web3.to_checksum_address("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599")
wbtc_abi = '[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_token","type":"address"}],"name":"reclaimToken","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"value","type":"uint256"}],"name":"burn","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"claimOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_subtractedValue","type":"uint256"}],"name":"decreaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_addedValue","type":"uint256"}],"name":"increaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"pendingOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"burner","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"}],"name":"OwnershipRenounced","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"},{"indexed":true,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]'  # noqa
wbtc_contract = w3.eth.contract(address=wbtc_address, abi=wbtc_abi)

uni_address = Web3.to_checksum_address("0x1f9840a85d5af5bf1d1762f925bdaddc4201f984")
uni_abi = '[{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"minter_","type":"address"},{"internalType":"uint256","name":"mintingAllowedAfter_","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegator","type":"address"},{"indexed":true,"internalType":"address","name":"fromDelegate","type":"address"},{"indexed":true,"internalType":"address","name":"toDelegate","type":"address"}],"name":"DelegateChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegate","type":"address"},{"indexed":false,"internalType":"uint256","name":"previousBalance","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newBalance","type":"uint256"}],"name":"DelegateVotesChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"minter","type":"address"},{"indexed":false,"internalType":"address","name":"newMinter","type":"address"}],"name":"MinterChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DELEGATION_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"DOMAIN_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint32","name":"","type":"uint32"}],"name":"checkpoints","outputs":[{"internalType":"uint32","name":"fromBlock","type":"uint32"},{"internalType":"uint96","name":"votes","type":"uint96"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"delegatee","type":"address"}],"name":"delegate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"delegatee","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"delegateBySig","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"delegates","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getCurrentVotes","outputs":[{"internalType":"uint96","name":"","type":"uint96"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"blockNumber","type":"uint256"}],"name":"getPriorVotes","outputs":[{"internalType":"uint96","name":"","type":"uint96"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"minimumTimeBetweenMints","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"mint","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"mintCap","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"minter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"mintingAllowedAfter","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"numCheckpoints","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"minter_","type":"address"}],"name":"setMinter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"src","type":"address"},{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'  # noqa
uni_contract = w3.eth.contract(address=uni_address, abi=uni_abi)

# Instantiate SDK
codec = RouterCodec()

# Pools
eth_wbtc_pool_key = codec.encode.v4_pool_key(eth_address, wbtc_address, 3000, 60)
eth_wbtc_pool_id = codec.encode.v4_pool_id(eth_wbtc_pool_key)

uni_wbtc_pool_key = codec.encode.v4_pool_key(uni_address, wbtc_address, 2500, 50)
uni_wbtc_pool_id = codec.encode.v4_pool_id(uni_wbtc_pool_key)

print("eth_wbtc_pool_id", eth_wbtc_pool_id.hex())
assert eth_wbtc_pool_id.hex().upper() == "54C72C46DF32F2CC455E84E41E191B26ED73A29452CDD3D82F511097AF9F427E"

# Uniswap contracts
ur_address = Web3.to_checksum_address("0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af")
permit2_address = Web3.to_checksum_address("0x000000000022D473030F116dDEE9F6B43aC78BA3")
posm_address = Web3.to_checksum_address("0xbD216513d74C8cf14cf4747E6AaA6420FF64ee9e")

v4_state_view_address = Web3.to_checksum_address("0x7fFE42C4a5DEeA5b0feC41C94C136Cf115597227")
v4_state_view_abi = '[{"inputs":[{"internalType":"contract IPoolManager","name":"_poolManager","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"PoolId","name":"poolId","type":"bytes32"}],"name":"getFeeGrowthGlobals","outputs":[{"internalType":"uint256","name":"feeGrowthGlobal0","type":"uint256"},{"internalType":"uint256","name":"feeGrowthGlobal1","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"PoolId","name":"poolId","type":"bytes32"},{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"}],"name":"getFeeGrowthInside","outputs":[{"internalType":"uint256","name":"feeGrowthInside0X128","type":"uint256"},{"internalType":"uint256","name":"feeGrowthInside1X128","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"PoolId","name":"poolId","type":"bytes32"}],"name":"getLiquidity","outputs":[{"internalType":"uint128","name":"liquidity","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"PoolId","name":"poolId","type":"bytes32"},{"internalType":"bytes32","name":"positionId","type":"bytes32"}],"name":"getPositionInfo","outputs":[{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256","name":"feeGrowthInside0LastX128","type":"uint256"},{"internalType":"uint256","name":"feeGrowthInside1LastX128","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"PoolId","name":"poolId","type":"bytes32"},{"internalType":"address","name":"owner","type":"address"},{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"bytes32","name":"salt","type":"bytes32"}],"name":"getPositionInfo","outputs":[{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256","name":"feeGrowthInside0LastX128","type":"uint256"},{"internalType":"uint256","name":"feeGrowthInside1LastX128","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"PoolId","name":"poolId","type":"bytes32"},{"internalType":"bytes32","name":"positionId","type":"bytes32"}],"name":"getPositionLiquidity","outputs":[{"internalType":"uint128","name":"liquidity","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"PoolId","name":"poolId","type":"bytes32"}],"name":"getSlot0","outputs":[{"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"},{"internalType":"int24","name":"tick","type":"int24"},{"internalType":"uint24","name":"protocolFee","type":"uint24"},{"internalType":"uint24","name":"lpFee","type":"uint24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"PoolId","name":"poolId","type":"bytes32"},{"internalType":"int16","name":"tick","type":"int16"}],"name":"getTickBitmap","outputs":[{"internalType":"uint256","name":"tickBitmap","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"PoolId","name":"poolId","type":"bytes32"},{"internalType":"int24","name":"tick","type":"int24"}],"name":"getTickFeeGrowthOutside","outputs":[{"internalType":"uint256","name":"feeGrowthOutside0X128","type":"uint256"},{"internalType":"uint256","name":"feeGrowthOutside1X128","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"PoolId","name":"poolId","type":"bytes32"},{"internalType":"int24","name":"tick","type":"int24"}],"name":"getTickInfo","outputs":[{"internalType":"uint128","name":"liquidityGross","type":"uint128"},{"internalType":"int128","name":"liquidityNet","type":"int128"},{"internalType":"uint256","name":"feeGrowthOutside0X128","type":"uint256"},{"internalType":"uint256","name":"feeGrowthOutside1X128","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"PoolId","name":"poolId","type":"bytes32"},{"internalType":"int24","name":"tick","type":"int24"}],"name":"getTickLiquidity","outputs":[{"internalType":"uint128","name":"liquidityGross","type":"uint128"},{"internalType":"int128","name":"liquidityNet","type":"int128"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolManager","outputs":[{"internalType":"contract IPoolManager","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'  # noqa
v4_state_view_contract = w3.eth.contract(address=v4_state_view_address, abi=v4_state_view_abi)


# Tests
def launch_anvil():
    anvil_process = subprocess.Popen(
        " ".join(
            [
                "anvil -vvvvv",
                f"--fork-url {web3_provider}",
                f"--fork-block-number {initial_block_number}",
                "--mnemonic-seed-unsafe 8721345628937456298",
            ]
        ),
        shell=True,
    )
    time.sleep(2)
    parent_id = anvil_process.pid
    return parent_id


def kill_processes(parent_id):
    processes = [str(parent_id), ]
    pgrep_process = subprocess.run(
        f"pgrep -P {parent_id}", shell=True, text=True, capture_output=True
    ).stdout.strip("\n")
    children_ids = pgrep_process.split("\n") if len(pgrep_process) > 0 else []
    processes.extend(children_ids)
    print(f"Killing processes: {' '.join(processes)}")
    subprocess.run(f"kill {' '.join(processes)}", shell=True, text=True, capture_output=True)


def check_initialization():
    assert w3.eth.chain_id == chain_id
    assert w3.eth.block_number == initial_block_number
    assert w3.eth.get_balance(account.address) == 10000 * 10**18
    assert wbtc_contract.functions.balanceOf(account.address).call() == 0
    print(" => Initialization: OK")


def swap_exact_in_single_eth_to_wbtc():
    print("START SWAP EXACT IN SINGLE ETH -> BTC")
    eth_amount = Wei(10 * 10**18)
    trx_params = (
        codec.
        encode.
        chain().
        v4_swap().
        swap_exact_in_single(
            pool_key=eth_wbtc_pool_key,
            zero_for_one=True,
            amount_in=eth_amount,
            amount_out_min=Wei(27000000),
        ).
        take_all(wbtc_address, Wei(0)).
        settle_all(eth_address, eth_amount).  # or: settle(eth_address, V4Constants.OPEN_DELTA.value, True).
        build_v4_swap().
        build_transaction(account.address, eth_amount, block_identifier=w3.eth.block_number)
    )
    raw_transaction = w3.eth.account.sign_transaction(trx_params, account.key).raw_transaction
    trx_hash = w3.eth.send_raw_transaction(raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(trx_hash)
    assert receipt["status"] == 1, f'receipt["status"] is actually {receipt["status"]}'  # status == 1 => trx success

    eth_balance = w3.eth.get_balance(account.address)
    print("ETH balance:", eth_balance / 10**18)
    wbtc_balance = wbtc_contract.functions.balanceOf(account.address).call()
    print("WBTC balance:", wbtc_balance / 10 ** 8)
    assert wbtc_balance == 27387998

    print("SWAP EXACT IN SINGLE ETH => OK\n")


def swap_exact_out_single_eth_to_wbtc():
    print("START SWAP EXACT OUT SINGLE ETH -> BTC")
    eth_amount_max = Wei(100 * 10 ** 18)
    wbtc_amount = Wei(27000000)

    trx_params = (
        codec.
        encode.
        chain().
        v4_swap().
        swap_exact_out_single(
            pool_key=eth_wbtc_pool_key,
            zero_for_one=True,
            amount_in_max=eth_amount_max,
            amount_out=wbtc_amount
        ).
        take_all(wbtc_address, wbtc_amount).
        settle_all(eth_address, eth_amount_max).  # or: settle(eth_address, V4Constants.OPEN_DELTA.value, True).
        build_v4_swap().
        sweep(FunctionRecipient.SENDER, eth_address, Wei(0)).  # Otherwise ETH stays on the contract
        build_transaction(account.address, eth_amount_max, block_identifier=w3.eth.block_number)
    )

    raw_transaction = w3.eth.account.sign_transaction(trx_params, account.key).raw_transaction
    trx_hash = w3.eth.send_raw_transaction(raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(trx_hash)
    assert receipt["status"] == 1, f'receipt["status"] is actually {receipt["status"]}'  # status == 1 => trx success

    eth_balance = w3.eth.get_balance(account.address)
    print("ETH balance:", eth_balance / 10 ** 18)
    wbtc_balance = wbtc_contract.functions.balanceOf(account.address).call()
    print("WBTC balance:", wbtc_balance / 10 ** 8)
    assert wbtc_balance == 27387998 + 27000000

    print("SWAP EXACT OUT SINGLE ETH => OK\n")


def init_v4_pool():
    print("START INIT V4 WBTC/UNI POOL")
    slot_0 = v4_state_view_contract.functions.getSlot0(uni_wbtc_pool_id).call()
    print(f"{slot_0=}")
    assert slot_0 == [0, 0, 0, 0]  # sqrtPriceX96 uint160, tick int24, protocolFee uint24, lpFee uint24

    trx_params = (
        codec
        .encode
        .chain()
        .v4_initialize_pool(uni_wbtc_pool_key, 10**14, 1)
        .build_transaction(account.address, Wei(100 * 10 ** 18), block_identifier=w3.eth.block_number)
    )

    raw_transaction = w3.eth.account.sign_transaction(trx_params, account.key).raw_transaction
    trx_hash = w3.eth.send_raw_transaction(raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(trx_hash)
    assert receipt["status"] == 1, f'receipt["status"] is actually {receipt["status"]}'  # status == 1 => trx success

    slot_0 = v4_state_view_contract.functions.getSlot0(uni_wbtc_pool_id).call()
    print(f"{slot_0=}")
    # sqrtPriceX96 uint160, tick int24, protocolFee uint24, lpFee uint24
    assert slot_0 == [7922816251426433400832, -322379, 0, 2500]

    liquidity = v4_state_view_contract.functions.getLiquidity(uni_wbtc_pool_id).call()
    assert liquidity == 0

    print("INIT V4 WBTC/UNI POOL => OK\n")


def permit2_ur(token_address):
    print(f"START PERMIT2 UNIVERSAL ROUTER for token: {token_address}")

    data, signable_message = codec.create_permit2_signable_message(
        token_address,
        2 ** 160 - 1,  # max = 2**160 - 1
        codec.get_default_expiration(),
        0,
        ur_address,  # The UR checksum address
        codec.get_default_deadline(30 * 24 * 3600),
        chain_id,
    )
    signed_message = account.sign_message(signable_message)
    trx_params = (
        codec.
        encode.
        chain().
        permit2_permit(data, signed_message).
        build_transaction(account.address, block_identifier=w3.eth.block_number)
    )

    raw_transaction = w3.eth.account.sign_transaction(trx_params, account.key).raw_transaction
    trx_hash = w3.eth.send_raw_transaction(raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(trx_hash)
    assert receipt["status"] == 1, f'receipt["status"] is actually {receipt["status"]}'  # status == 1 => trx success

    permit2_allowance = codec.fetch_permit2_allowance(account.address, token_address, ur_address)
    print(permit2_allowance)
    assert permit2_allowance[0] == 1461501637330902918203684832716283019655932542975
    assert permit2_allowance[1] > 1737644220
    assert permit2_allowance[2] == 1

    print(f"PERMIT2 UNIVERSAL ROUTER for token: {token_address} => OK\n")


def approve_permit2_for_token(token_contract):
    print(f"START APPROVE PERMIT2 FOR token: {token_contract.address}")
    contract_function = token_contract.functions.approve(permit2_address, 2 ** 256 - 1)
    trx_params = contract_function.build_transaction(
        {
            "from": account.address,
            "gas": 800_000,
            "maxPriorityFeePerGas": w3.eth.max_priority_fee,
            "maxFeePerGas": Wei(10 * 10 ** 9),
            "type": '0x2',
            "chainId": chain_id,
            "value": 0,
            "nonce": w3.eth.get_transaction_count(account.address),
        }
    )

    raw_transaction = w3.eth.account.sign_transaction(trx_params, account.key).raw_transaction
    trx_hash = w3.eth.send_raw_transaction(raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(trx_hash)
    assert receipt["status"] == 1, f'receipt["status"] is actually {receipt["status"]}'  # status == 1 => trx success

    allowance = token_contract.functions.allowance(account.address, permit2_address).call()
    print(allowance)
    assert allowance in (2 ** 256 - 1, 2**96 - 1)  # UNI max allowance is 2**96 - 1

    print(f"APPROVE PERMIT2 FOR token: {token_contract.address} => OK\n")


def mint_v4_position():
    print("START MINT V4 POSITION")

    uni_balance = uni_contract.functions.balanceOf(account.address).call()
    print(f"{uni_balance=}", uni_balance / 10 ** 18)

    wbtc_balance = wbtc_contract.functions.balanceOf(account.address).call()
    print(f"{wbtc_balance=}", wbtc_balance / 10 ** 8)

    weth_uni_v3_path = [weth_address, 3000, uni_address]

    trx_params = (
        codec.
        encode.
        chain().
        wrap_eth(FunctionRecipient.ROUTER, Wei(20 * 10 ** 18)).
        v3_swap_exact_in_from_balance(FunctionRecipient.ROUTER, Wei(5000 * 10**18), weth_uni_v3_path).
        transfer(FunctionRecipient.CUSTOM, uni_address, Wei(5000 * 10**18), posm_address).
        permit2_transfer_from(FunctionRecipient.CUSTOM, wbtc_address, Wei(int(0.5 * 10**8)), posm_address).
        v4_posm_call().
        mint_position(
            pool_key=uni_wbtc_pool_key,
            tick_lower=(-322379 - 10 * 50) // 50 * 50,
            tick_upper=(-322379 + 10 * 50) // 50 * 50,
            liquidity=int(1.8 * 10**16),
            amount_0_max=5000 * 10**18,
            amount_1_max=int(0.5 * 10**8),
            recipient=account.address,
            hook_data=b"",
        ).
        settle(uni_address, V4Constants.OPEN_DELTA.value, False).
        settle(wbtc_address, V4Constants.OPEN_DELTA.value, False).

        sweep(uni_address, account.address).
        sweep(wbtc_address, account.address).
        sweep(eth_address, account.address).
        build_v4_posm_call(codec.get_default_deadline()).
        sweep(FunctionRecipient.SENDER, uni_address, Wei(0)).
        build_transaction(account.address, Wei(20 * 10 ** 18), block_identifier=w3.eth.block_number)
    )

    raw_transaction = w3.eth.account.sign_transaction(trx_params, account.key).raw_transaction
    trx_hash = w3.eth.send_raw_transaction(raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(trx_hash)
    assert receipt["status"] == 1, f'receipt["status"] is actually {receipt["status"]}'  # status == 1 => trx success

    assert weth_contract.functions.balanceOf(account.address).call() == 0  # 100 * 10**18

    new_uni_balance = uni_contract.functions.balanceOf(account.address).call()
    print(f"{new_uni_balance=}", new_uni_balance / 10**18)
    assert new_uni_balance == 1214600561839991914502

    new_wbtc_balance = wbtc_contract.functions.balanceOf(account.address).call()
    print(f"{new_wbtc_balance=}", new_wbtc_balance / 10 ** 8, "diff:", (wbtc_balance - new_wbtc_balance))
    assert new_wbtc_balance == 8020780


def swap_exact_in_eth_to_uni():
    print("START SWAP IN THROUGH 2 POOLS (ETH -> WBTC -> UNI)")
    path_key_eth_wbtc = codec.encode.v4_path_key(
        wbtc_address,
        3000,
        60,
    )
    path_key_wbtc_uni = codec.encode.v4_path_key(
        uni_address,
        2500,
        50,
    )

    amount_in = Wei(1 * 10**18)

    trx_params = (
        codec.
        encode.
        chain().
        v4_swap().
        swap_exact_in(
            eth_address,
            [path_key_eth_wbtc, path_key_wbtc_uni],
            amount_in,
            Wei(0),
        ).
        settle_all(eth_address, amount_in).  # or settle(eth_address, amount_in, True).
        take_all(uni_address, 0).  # or take(uni_address, account.address, 0).
        build_v4_swap().
        build_transaction(
            account.address,
            amount_in,
            block_identifier=w3.eth.block_number,
        )
    )
    raw_transaction = w3.eth.account.sign_transaction(trx_params, account.key).raw_transaction
    trx_hash = w3.eth.send_raw_transaction(raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(trx_hash)
    assert receipt["status"] == 1, f'receipt["status"] is actually {receipt["status"]}'  # status == 1 => trx success

    new_uni_balance = uni_contract.functions.balanceOf(account.address).call()
    print(f"{new_uni_balance=}", new_uni_balance / 10 ** 18)
    assert new_uni_balance == 1486418967458590004944

    print("SWAP IN THROUGH 2 POOLS (ETH -> WBTC -> UNI) => OK")


def swap_exact_out_uni_to_eth():
    print("START SWAP OUT THROUGH 2 POOLS (UNI -> WBTC -> ETH)")
    eth_balance = w3.eth.get_balance(account.address)
    print("ETH balance:", eth_balance / 10 ** 18)

    path_key_eth_wbtc = codec.encode.v4_path_key(
        wbtc_address,
        3000,
        60,
    )
    path_key_wbtc_uni = codec.encode.v4_path_key(
        uni_address,
        2500,
        50,
    )

    amount_out = Wei(1 * 10 ** 18)  # 1 ETH out

    trx_params = (
        codec.
        encode.
        chain().
        v4_swap().
        swap_exact_out(
            eth_address,
            [path_key_wbtc_uni, path_key_eth_wbtc],
            amount_out,
            Wei(300 * 10**18),  # max 300 UNI in
        ).
        settle_all(uni_address, 300 * 10**18).
        take_all(eth_address, 0).  # or take(eth_address, account.address, amount_out).
        build_v4_swap().
        build_transaction(
            account.address,
            0,
            block_identifier=w3.eth.block_number,
        )
    )

    raw_transaction = w3.eth.account.sign_transaction(trx_params, account.key).raw_transaction
    trx_hash = w3.eth.send_raw_transaction(raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(trx_hash)
    assert receipt["status"] == 1, f'receipt["status"] is actually {receipt["status"]}'  # status == 1 => trx success

    new_uni_balance = uni_contract.functions.balanceOf(account.address).call()
    print(f"{new_uni_balance=}", new_uni_balance / 10 ** 18)
    assert new_uni_balance == 1211586049451302584537 < 1214600561839991914502

    new_eth_balance = w3.eth.get_balance(account.address)
    print("New ETH balance:", new_eth_balance / 10 ** 18)
    assert new_eth_balance - eth_balance > 0.99 * 10**18

    print("SWAP OUT THROUGH 2 POOLS (UNI -> WBTC -> ETH) => OK")


def launch_integration_tests():
    print("------------------------------------------")
    print("| Launching integration tests            |")
    print("------------------------------------------")
    check_initialization()
    swap_exact_in_single_eth_to_wbtc()
    swap_exact_out_single_eth_to_wbtc()
    init_v4_pool()

    permit2_ur(wbtc_address)
    permit2_ur(uni_address)
    approve_permit2_for_token(wbtc_contract)
    approve_permit2_for_token(uni_contract)
    mint_v4_position()

    swap_exact_in_eth_to_uni()
    swap_exact_out_uni_to_eth()


def print_success_message():
    print("------------------------------------------")
    print("| Integration tests are successful !! :) |")
    print("------------------------------------------")


def main():
    anvil_pid = launch_anvil()
    try:
        launch_integration_tests()
        print_success_message()
    finally:
        kill_processes(anvil_pid)


if __name__ == "__main__":
    main()
