'''
Сети:
- Ethereum
- Arbitrum
- Optimism
- Polygon
- Avalanche
- Fantom
- Celo
- Klaytn
- Bsc
- Moonbeam
- Base
'''

FROM_CHAIN = 'Polygon' # Где минтить и откуда бриджить
TO_CHAIN = ['Celo', 'Klaytn', 'Fantom'] # Куда бриджить

WMERK_AMOUNT = [1, 2] # Кол-во токенов для минта и бриджа

SLEEPING_ACTIONS = [15, 60] # Спим между активностями на одном кошельке
SLEEPING_WALLETS = [60, 150] # Спим между работой кошельков

RANDOMISE_WALLETS = True # Рандомить кошельки