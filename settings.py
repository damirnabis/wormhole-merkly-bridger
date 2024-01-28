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

FROM_CHAIN = ['Polygon', 'Arbitrum', 'Optimism', 'Avalanche', 'Base', 'Bsc', 'Fantom'] # Где минтить и откуда бриджить. Рандомно выберит одну сеть из списка 

TO_CHAIN = ['Celo', 'Klaytn', 'Fantom', 'Moonbeam'] # Куда бриджить
TO_CHAIN_COUNT = [1, 4] # Укажи количество сетей куда бриджить, рандомно выберит из списка TO_CHAIN. Для бриджа во все сети из TO_CHAIN, укажи пустой список: TO_CHAIN_COUNT = []

WMERK_AMOUNT = [1, 2] # Кол-во токенов для минта и бриджа

SLEEPING_ACTIONS = [25, 100] # Спим между активностями на одном кошельке
SLEEPING_WALLETS = [100, 300] # Спим между работой кошельков

RANDOMISE_WALLETS = True # Рандомить кошельки

RETRY_COUNT = 3 # Количество попыток при возникновении ошибки

CHECK_GWEI = True # Контролировать текущий gas сети в майннете (True/False)
MAX_GAS_ETH = 21 # максимальный gas в gwei при котором будет выполняться скрипт, иначе ждет