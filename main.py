from utils import *
from client import Client
from config import *
from settings import *
from moduls.merkly import Merkly
from models import Ethereum, TokenAmount, get_network


def start_smart_mode(private_key):    
    from_chains_ids = []
    for from_chain in FROM_CHAIN:
        _, _, from_id = TOKENS_DATA[from_chain]
        from_chains_ids.append(from_id)
        
    to_chains_ids = []
    for to_chain in TO_CHAIN:
        _, _, to_id = TOKENS_DATA[to_chain]
        to_chains_ids.append(to_id)
        
    random.shuffle(from_chains_ids)
    random.shuffle(to_chains_ids)
        
    client = Client(private_key=private_key, network=Ethereum)
    
    address = client.address 
    
    logger.info(f'{address} | Choosing the optimal route...')
        
    url = f'https://api.wormholescan.io/api/v1/transactions/?address={address}'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        resp_json = response.json()
        resp_json_transactions = resp_json['transactions']
        chains_activity_data = {}
        
        # Получаем историю всех транзакций
        for i in range(0, len(resp_json_transactions)):
            emitterChain = resp_json_transactions[i]['emitterChain']
            toChain      = resp_json_transactions[i]['standardizedProperties']['toChain']
            
            if emitterChain in chains_activity_data:            
                chains_activity_data[emitterChain]['value'] += 1
                
                if toChain in chains_activity_data[emitterChain]['to_chains']:
                    chains_activity_data[emitterChain]['to_chains'][toChain]['value'] += 1
                
                else:
                    chains_activity_data[emitterChain]['to_chains'][toChain] = {'value': 1}                                      
            
            else:
                chains_activity_data[emitterChain] = {'value': 1, 'to_chains': {}}
                chains_activity_data[emitterChain]['to_chains'][toChain] = {'value': 1}
        
        # Убираем чейны, которые не указаны в настройках        
        chains_activity_data_keys = list(chains_activity_data.keys())
        
        for chains_activity_data_key in chains_activity_data_keys:
            
            if not chains_activity_data_key in from_chains_ids:
               del chains_activity_data[chains_activity_data_key]
               
            else:
                to_chains_activity_data_keys = list(chains_activity_data[chains_activity_data_key]['to_chains'].keys())
                
                for to_chain_activity_data_key in to_chains_activity_data_keys:
                    
                    if not to_chain_activity_data_key in to_chains_ids:
                        chains_activity_data[chains_activity_data_key]['value'] -= chains_activity_data[chains_activity_data_key]['to_chains'][to_chain_activity_data_key]['value']
                        del chains_activity_data[chains_activity_data_key]['to_chains'][to_chain_activity_data_key]
                
        # Добавляем чейны, которые указаны в настройках и по которым не было транзакций
        for from_chain_id in from_chains_ids:                  
            
            if not from_chain_id in chains_activity_data:
                chains_activity_data[from_chain_id] = {'value': 0, 'to_chains': {}}
             
            for to_chain_id in to_chains_ids:   
                
                if not to_chain_id in chains_activity_data[from_chain_id]['to_chains']:
                    chains_activity_data[from_chain_id]['to_chains'][to_chain_id] = {'value': 0} 
        
        # Определяем чейны с наименьшими транзакциями
        interaction_summary_sheet = {}
        
        sorted_from_chains_activity_data = sorted(chains_activity_data.items(), key=lambda item: item[1]['value'])
        
        low_txs_value_from_chain = sorted_from_chains_activity_data[0][1]['value']
        
        for from_chain_activity_data in sorted_from_chains_activity_data:

            if from_chain_activity_data[1]['value'] == low_txs_value_from_chain:
                from_chain_id = from_chain_activity_data[0]
                
                interaction_summary_sheet[from_chain_id] = []
                
                sorted_to_chains_activity_data = sorted(chains_activity_data[from_chain_activity_data[0]]['to_chains'].items(), key=lambda item: item[1]['value'])

                low_txs_value_to_chain = sorted_to_chains_activity_data[0][1]['value']
                
                for to_chain_activity_data in sorted_to_chains_activity_data:
                    
                    if to_chain_activity_data[1]['value'] == low_txs_value_to_chain:
                        to_chain_id = to_chain_activity_data[0]
                        
                        interaction_summary_sheet[from_chain_id].append(to_chain_id)
        
        # Минт + бридж                                              
        tx_count = random.randint(TX_COUNT[0], TX_COUNT[1])
        
        i=0
        while i < tx_count:
            if len(interaction_summary_sheet) == 0: break
            
            choosen_from_chain_id = random.choice(list(interaction_summary_sheet.keys()))
            choosen_to_chain_id = random.choice(interaction_summary_sheet[choosen_from_chain_id])
            
            interaction_summary_sheet[choosen_from_chain_id].remove(choosen_to_chain_id)
            
            if len(interaction_summary_sheet[choosen_from_chain_id]) == 0:
                del interaction_summary_sheet[choosen_from_chain_id]
                
            wft_mint_bridge(private_key, CHAINS_ID[choosen_from_chain_id], [CHAINS_ID[choosen_to_chain_id]])
                       
            i+=1
                    
    else:
        logger.error(f'{address} | Error code: {response.status_code}. Failed to receive transactions.')
        

def start_standard_mode(private_key):
    from_chain = random.choice(FROM_CHAIN)
        
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
        
        to_chain_count = random.randint(to_chain_count_first, to_chain_count_last)
        
        to_chains = []
        for i in range(1, to_chain_count+1):
            chain_to = random.choice(to_chain_list)
            to_chains.append(chain_to)
            
    else:
        to_chains = TO_CHAIN        
            
    random.shuffle(to_chains)
    
    wft_mint_bridge(private_key, from_chain, to_chains)                                                               

 
def wft_mint_bridge(private_key, from_chain, to_chains):
    from_contract, mint_value, _ = TOKENS_DATA[from_chain]
    
    client = Client(private_key=private_key, network=get_network(from_chain))
       
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
        
        if SMART_MODE:
            logger.info(f'START SMART MODE')
            
            start_smart_mode(private_key)
                   
        else:
            logger.info(f'START STANDART MODE')
            
            start_standard_mode(private_key)
        
        sleep(SLEEPING_WALLETS[0], SLEEPING_WALLETS[1])
                  

if __name__ == '__main__': 
    main()

    
