from dataclasses import dataclass
from decimal import Decimal
from typing import Union


@dataclass
class DefaultABIs:
    """
    The default ABIs.
    """
    Token = [
        {
            'constant': True,
            'inputs': [],
            'name': 'name',
            'outputs': [{'name': '', 'type': 'string'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'symbol',
            'outputs': [{'name': '', 'type': 'string'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'totalSupply',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'decimals',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [{'name': 'who', 'type': 'address'}],
            'name': 'balanceOf',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [{'name': '_owner', 'type': 'address'}, {'name': '_spender', 'type': 'address'}],
            'name': 'allowance',
            'outputs': [{'name': 'remaining', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': False,
            'inputs': [{'name': '_spender', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],
            'name': 'approve',
            'outputs': [],
            'payable': False,
            'stateMutability': 'nonpayable',
            'type': 'function'
        },
        {
            'constant': False,
            'inputs': [{'name': '_to', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],
            'name': 'transfer',
            'outputs': [], 'payable': False,
            'stateMutability': 'nonpayable',
            'type': 'function'
        }]


class TokenAmount:
    Wei: int
    Ether: Decimal
    decimals: int

    def __init__(self, amount: Union[int, float, str, Decimal], decimals: int = 18, wei: bool = False) -> None:
        if wei:
            self.Wei: int = amount
            self.Ether: Decimal = Decimal(str(amount)) / 10 ** decimals

        else:
            self.Wei: int = int(Decimal(str(amount)) * 10 ** decimals)
            self.Ether: Decimal = Decimal(str(amount))

        self.decimals = decimals


class Network:
    def __init__(self,
                 name: str,
                 rpc: str,
                 chain_id: int,
                 eip1559_tx: bool,
                 coin_symbol: str,
                 explorer: str,
                 decimals: int = 18,
                 ):
        self.name = name
        self.rpc = rpc
        self.chain_id = chain_id
        self.eip1559_tx = eip1559_tx
        self.coin_symbol = coin_symbol
        self.decimals = decimals
        self.explorer = explorer

    def __str__(self):
        return f'{self.name}'
    

Ethereum = Network(
    name='ethereum',
    rpc='https://mainnet.infura.io/v3/',
    chain_id=1,
    eip1559_tx=True,
    coin_symbol='ETH',
    explorer='https://etherscan.io/',
)


Arbitrum = Network(
    name='arbitrum',
    rpc='https://rpc.ankr.com/arbitrum/',
    chain_id=42161,
    eip1559_tx=True,
    coin_symbol='ETH',
    explorer='https://arbiscan.io/',
)


Optimism = Network(
    name='optimism',
    rpc='https://rpc.ankr.com/optimism/',
    chain_id=10,
    eip1559_tx=True,
    coin_symbol='ETH',
    explorer='https://optimistic.etherscan.io/',
)


Polygon = Network(
    name='polygon',
    rpc='https://polygon-rpc.com/',
    chain_id=137,
    eip1559_tx=True,
    coin_symbol='MATIC',
    explorer='https://polygonscan.com/',
)


Avalanche = Network(
    name='avalanche',
    rpc='https://rpc.ankr.com/avalanche/',
    chain_id=43114,
    eip1559_tx=True,
    coin_symbol='AVAX',
    explorer='https://snowtrace.io/',
)


Fantom = Network(
    name='fantom',
    rpc='https://rpc.ankr.com/fantom/',
    chain_id=250,
    eip1559_tx=True,
    coin_symbol='FTM',
    explorer='https://ftmscan.com/',
)


Celo = Network(
    name='celo',
    rpc='https://forno.celo.org',
    chain_id=42220,
    eip1559_tx=True,
    coin_symbol='CELO',
    explorer='https://explorer.celo.org/mainnet/',
)


Klaytn = Network(
    name='klaytn',
    rpc='https://public-en-cypress.klaytn.net/',
    chain_id=8217,
    eip1559_tx=True,
    coin_symbol='KLAY',
    explorer='https://klaytnscope.com/',
)


Bsc = Network(
    name='bsc',
    rpc='https://rpc.ankr.com/bsc/',
    chain_id=56,
    eip1559_tx=True,
    coin_symbol='BNB',
    explorer='https://bscscan.com/',
)


Moonbeam = Network(
    name='moonbeam',
    rpc='https://rpc.api.moonbeam.network',
    chain_id=1284,
    eip1559_tx=True,
    coin_symbol='GLMR',
    explorer='https://moonscan.io/',
)


Base = Network(
    name='base',
    rpc='https://developer-access-mainnet.base.org',
    chain_id=8453,
    eip1559_tx=True,
    coin_symbol='ETH',
    explorer='https://basescan.org/',
)


def get_network(network_name: str):
    network_name = network_name.lower()
    
    if network_name == 'ethereum':
        return Ethereum
    elif network_name == 'arbitrum':
        return Arbitrum
    elif network_name == 'optimism':
        return Optimism
    elif network_name == 'polygon':
        return Polygon
    elif network_name == 'avalanche':
        return Avalanche
    elif network_name == 'fantom':
        return Fantom
    elif network_name == 'celo':
        return Celo
    elif network_name == 'klaytn':
        return Klaytn
    elif network_name == 'bsc':
        return Bsc
    elif network_name == 'moonbeam':
        return Moonbeam
    elif network_name == 'base':
        return Base
    else:
        return None