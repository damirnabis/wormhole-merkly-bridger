from utils import *
from client import Client
from config import *
from settings import *
from moduls.merkly import Merkly
from models import TokenAmount, get_network
 
 
def wft_mint_bridge(private_key):
    from_chain = FROM_CHAIN
    from_contract, mint_value, _ = TOKENS_DATA[from_chain]
    
    client = Client(private_key=private_key, network=get_network(from_chain))
    
    to_chain_list = TO_CHAIN
    if from_chain in to_chain_list:
        to_chain_list.remove(from_chain)
    
    random.shuffle(to_chain_list) 
       
    for to_chain in to_chain_list:
        merkly = Merkly(client=client, router_address=from_contract)
        
        to_contract, _, to_id = TOKENS_DATA[to_chain]
        wmerk_amount = random.randint(WMERK_AMOUNT[0], WMERK_AMOUNT[1])
          
        logger.info(f'{client.address} | Mint {wmerk_amount} wmerk in {from_chain}')
    
        tx = merkly.mint_wmerk(TokenAmount(amount=mint_value), wmerk_amount)
        res = client.verif_tx(tx_hash=tx)
    
        if res==False:
            continue
                 
        sleep(5, 15)
    
        logger.info(f'{client.address} | Bridge {wmerk_amount} wmerk from {from_chain} to {to_chain}')
    
        tx = merkly.bridge_wmerk(to_contract, to_id, TokenAmount(amount=wmerk_amount))
        res = client.verif_tx(tx_hash=tx)
    
        if res==False:
            continue
        
        sleep(SLEEPING_ACTIONS[0], SLEEPING_ACTIONS[1])
              
 
def main():
    with open ('private_keys.txt', 'r', encoding='utf-8') as f: 
        private_keys = f.read().splitlines()
        
    if RANDOMISE_WALLETS:
        random.shuffle(private_keys)    
    
    for private_key in private_keys:
        wft_mint_bridge(private_key)
        
        sleep(SLEEPING_WALLETS[0], SLEEPING_WALLETS[1])
                  

if __name__ == '__main__': 
    main()

    
