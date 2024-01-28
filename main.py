from utils import *
from client import Client
from config import *
from settings import *
from moduls.merkly import Merkly
from models import TokenAmount, get_network
 
 
def wft_mint_bridge(private_key):
    from_chain = random.choice(FROM_CHAIN)
    from_contract, mint_value, _ = TOKENS_DATA[from_chain]
    
    client = Client(private_key=private_key, network=get_network(from_chain))
    
    to_chain_list = TO_CHAIN
    if len(TO_CHAIN_COUNT) > 1:
        to_chain_count_first = TO_CHAIN_COUNT[0]
        to_chain_count_last  = TO_CHAIN_COUNT[1]
        to_chain_list_quantity = len(to_chain_list)   
    
        if to_chain_list_quantity == 1:
            to_chain_count_first = 1
            to_chain_count_last = 1
        
        if to_chain_list_quantity < to_chain_count_first:
            to_chain_count_first = 1
    
        if to_chain_list_quantity < to_chain_count_last:
            to_chain_count_last = to_chain_list_quantity  
        
        if from_chain in to_chain_list:
            to_chain_list.remove(from_chain)   
        
        to_chain_count = random.randint(to_chain_count_first, to_chain_list_quantity)
        
        to_chains = []
        for i in range(1, to_chain_count+1):
            chain_to = random.choice(to_chain_list)
            to_chains.append(chain_to)
            
    else:
        to_chains = TO_CHAIN        
            
    random.shuffle(to_chains)
       
    for to_chain in to_chains:
        merkly = Merkly(client=client, router_address=from_contract)
        
        to_contract, _, to_id = TOKENS_DATA[to_chain]
        wmerk_amount = random.randint(WMERK_AMOUNT[0], WMERK_AMOUNT[1])
          
        logger.info(f'{client.address} | Mint {wmerk_amount} wmerk in {from_chain}')
        
        for i in range(1, RETRY_COUNT+1):
            try:
                tx = merkly.mint_wmerk(TokenAmount(amount=mint_value), wmerk_amount)
                res = client.verif_tx(tx_hash=tx)
                break
            except:
                logger.info(f'Trying {i}/{RETRY_COUNT}...')                   
    
        if res==False:                 
            continue
                 
        sleep(5, 25)
    
        logger.info(f'{client.address} | Bridge {wmerk_amount} wmerk from {from_chain} to {to_chain}')
        
        for i in range(1, RETRY_COUNT+1):
            try:
                tx = merkly.bridge_wmerk(to_contract, to_id, TokenAmount(amount=wmerk_amount))                  
                res = client.verif_tx(tx_hash=tx)
                break
            except:
                logger.info(f'Trying {i}/{RETRY_COUNT}...')
    
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

    
