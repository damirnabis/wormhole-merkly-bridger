from utils import *
from client import Client
from config import MERKLY_ABI
from utils import read_json
from models import TokenAmount


class Merkly:
    def __init__(self, client: Client, router_address):
        self.client = client
        self.router_abi = MERKLY_ABI['WOFT']
        self.router_address = Web3.to_checksum_address(router_address)
        self.contract = self.client.w3.eth.contract(abi=self.router_abi, address=self.router_address)
        
    def get_estimate_fee(self, to_id):      
        estimate_fee = self.contract.functions.quoteBridge(
                                            to_id,                                              
                                            0,                                                                    
                                            200000
                                        ).call()
        return estimate_fee[0]     
        
    def mint_wmerk(self, mint_value: TokenAmount, wmerk_amount):
        return self.client.send_transaction(
            to=self.router_address,
            data=self.contract.encodeABI('mint',
                                    args=(
                                        self.client.address,
                                        wmerk_amount
                                    )),
            value=mint_value.Wei * wmerk_amount
        )

    def bridge_wmerk(self, to_contract, to_id, wmerk_amount: TokenAmount):
        return self.client.send_transaction(
            to=self.router_address,
            data=self.contract.encodeABI('bridge',
                                    args=(
                                        to_id,
                                        to_contract,
                                        wmerk_amount.Wei,
                                        0,
                                        200000,
                                        to_id,
                                        self.client.address                                        
                                    )),
            value=self.get_estimate_fee(to_id)
        )