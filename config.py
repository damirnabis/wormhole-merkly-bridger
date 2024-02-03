import os
import sys
from pathlib import Path


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.absolute()

ABIS_DIR = os.path.join(ROOT_DIR, 'abis')

TOKEN_ABI = os.path.join(ABIS_DIR, 'token.json')
#MERKLY_ABI = os.path.join(ABIS_DIR, 'merkly.json')
MERKLY_ABI = {'WOFT': [{'constant': True, 'inputs': [{'name': 'targetChain', 'type': 'uint16'}, {'name': 'receiverValue', 'type': 'uint256'}, {'name': 'gasLimit', 'type': 'uint256'}], 'name': 'quoteBridge', 'outputs': [{'name': 'nativePriceQuote', 'type': 'uint256'}, {'name': 'targetChainRefundPerGasUnused', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'targetChain', 'type': 'uint16'}, {'name': 'targetAddress', 'type': 'address'}, {'name': 'amount', 'type': 'uint256'}, {'name': 'receiverValue', 'type': 'uint256'}, {'name': 'gasLimit', 'type': 'uint256'}, {'name': 'refundChain', 'type': 'uint16'}, {'name': 'refundAddress', 'type': 'address'}], 'name': 'bridge', 'outputs': [], 'payable': True, 'stateMutability': 'payable', 'type': 'function'}, {'constant': False, 'inputs': [{'name': '_to', 'type': 'address'}, {'name': '_amount', 'type': 'uint256'}], 'name': 'mint', 'outputs': [], 'payable': True, 'stateMutability': 'payable', 'type': 'function'}]}

TOKENS_DATA = {
    'Optimism' : ('0x660991a4e549B2032dCAF781b85a8FE1dF176BB6', 0.0000021, 24),
    'Celo': ('0x5c17938e1317a05682CC7026F63C0396C84706C8', 0.0089485, 14),
    'Avalanche': ('0x28527ebb5C97BB11aBd6c2C74D24045b4e4865eF', 0.00033, 6),
    'Klaytn': ('0x9AA7AC03CAA440c392B9C9D25a728b429E172a92', 0.027, 13),
    'Bsc': ('0x41cc0c5Dbd2539191945f395B17cEb597BCE1C9A', 0.0000201775, 4),
    'Moonbeam': ('0x3cc4313f8e5E413a54095D48DB1869f80f929056', 0.02, 16),
    'Fantom': ('0xCd8EAE908E27b9046ca7845DA22f6d3cdf367588', 0.018, 10),
    'Arbitrum' : ('0x456A5d70f5E1f23ec5B074144477817447551439', 0.0000021, 23),
    'Polygon' : ('0x81143d533675D79b490Bb3B3a00421b1CAEce3D9', 0.0063, 5),
    'Base' : ('0x2e3e4Cc4c99fEaac88097b1Bc279c7e372BfBdFE', 0.0000021, 30),
    'Ethereum': ('0xac998bda5B8bc9483c90eFBe8B70E11D3C0E8f6f', 0.0000021, 2),
}

CHAINS_ID = {
    24: 'Optimism',
    14: 'Celo',
    6: 'Avalanche',
    13: 'Klaytn',
    4: 'Bsc',
    16: 'Moonbeam',
    10: 'Fantom',
    23: 'Arbitrum',
    5: 'Polygon',
    30: 'Base',
    2: 'Ethereum'   
}