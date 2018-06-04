from bittrex import bittrex
from binance import Client
import operator,json, math, os

def read_config(exchange, param, template=0):
    if template == 0:
        with open('settings.js', 'r') as f:
            data = json.load(f)
        result = data[exchange][param]
        f.close()
    else:
        with open('template_' + exchange + '.js', 'r') as f:
            data = json.load(f)
        result = data['exchanges'][exchange][param]
        f.close()
    return result        

def list_coins_binance(key, secret, type):
    
    api = Client(key, secret)

    tableaux = api.get_ticker()
    balances = api.get_account()

    data={}
    balance_coins=[]
    contents=[]
    #print(balances['balances'][0]['free'])
    #####
    # Check coins availables with balances > 0.0
    #####
    for i in range(0, len(balances)):
        if float(balances['balances'][i]['free']) > 0.001 \
            and balances['balances'][i]['asset'] != 'BNB' \
            and balances['balances'][i]['asset'] != 'BTC':
            balance_coins.append(balances['balances'][i]['asset'])
    print('\n-----------------------Binance-------------------- \n')        
    print('... Bags Holder ... \n')
    print(balance_coins)
    ###
    # Construct list of coins to trade with volume criteria
    ###
    for i in range(0, len(tableaux)):
        if type in tableaux[i]['symbol'][-4:]:
            #print(tableaux[i]['symbol'][-4:] + '------' +tableaux[i]['quoteVolume'])
            data[tableaux[i]['symbol']] = float(tableaux[i]['quoteVolume'])
            sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)

    if int(read_config('binance', 'last_position')) > len(sorted_data):
        total = len(sorted_data)
    else:
        total = int(read_config('binance', 'last_position'))

    for i in range(int(read_config('binance', 'first_position')) -1, total):
        #print(sorted_data[i][0][:-3] + '-----' + str(sorted_data[i][1]))
        contents.append(sorted_data[i][0][:-len(type)])
    results = contents
    print('------------- Coins top ------------- \n')
    print(results)
    all_contents =''

    for result in balance_coins:
        all_contents += result + '\n'

    with open('bags_binance.txt', 'w', encoding='utf8') as f:
        f.write(all_contents)
    f.close()

    all_contents = ''

    for result in results:
        all_contents += result + '\n'

    with open('Choices_binance.txt', 'w', encoding='utf8') as f:
        f.write(all_contents)
    f.close()

    create_file_config(type)

def list_coins_bittrex(key, secret, type):
    
    api = bittrex(key, bytes(secret.encode("utf-8")))

    tableaux = api.getmarketsummaries()
    balances = api.getbalances()

    data={}
    balance_coins=[]
    contents=[]

    #####
    # Check coins availables with balances > 0.0
    #####
    for i in range(0, len(balances)):
        if float(balances[i]['Available']) > 0.001 \
            and balances[i]['Currency'] != 'BTC':
            balance_coins.append(balances[i]['Currency'])
    #print(balance_coins)  
    for i in range(0, len(balance_coins)):
        try:
            balance_buy_price = api.getorderhistory(type + '-' + balance_coins[i], 1)
            price_now = float('%.8f' % balance_buy_price[0]['PricePerUnit'])
            price_buy = float ('%.8f' % balance_buy_price[0]['Limit'])
            pourcentage = (price_now - price_buy) / price_buy * 100
            pourcentage = float ('%.8f' % pourcentage)
            print('%.2f' % pourcentage)
            balance_coins[i] += '   ->   ' + 'Price Now: ' + str('%.8f' % price_now) \
                                            + ' ### Price Buy: ' +  str('%.8f' % price_buy) \
                                             + ' ### Pourcentage: ' +str('%.2f' % pourcentage)
        except:
            pass
        

    print('----------------------Bittrex---------------------\n')        
    print('... Bags Holder... \n')

    ###
    # Construct list of coins to trade with volume criteria
    ###
    for i in range(0, len(tableaux)):

        if type in tableaux[i]['MarketName'][0:4] :
            #print(tableaux[i]['MarketName'])
            data[tableaux[i]['MarketName']] = tableaux[i]['BaseVolume']
            
    sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
    #print(sorted_data)
    if int(read_config('bittrex', 'last_position')) > len(sorted_data):
        total = len(sorted_data)
    else:
        total = int(read_config('bittrex', 'last_position'))

    for i in range(int(read_config('bittrex', 'first_position')) -1, total):
        #print(sorted_data[i][0][4:] + '-----' + str(sorted_data[i][1]))
        contents.append(sorted_data[i][0][sorted_data[i][0].index('-')+1:])

    #s_c_coins = set(contents)    
    #s_b_coins = set(balance_coins)
    #results = sorted(s_c_coins|s_b_coins) #union

    results = contents
    print('------------- Coins top ------------- \n')
    print(results)

    all_contents =''

    for result in balance_coins:
        all_contents += result + '\n'

    with open('bags_bittrex.txt', 'w', encoding='utf8') as f:
        f.write(all_contents)
    f.close()


    all_contents = ''
    for result in results:
        all_contents += result + '\n'

    with open('Choices_bittrex.txt', 'w', encoding='utf8') as f:
        f.write(all_contents)
    f.close()

    create_file_config(type)

def create_file_config(type): 
    for exchange in ('bittrex', 'binance'):
        #Select pairs
        pairs = []
        with open('Choices_' + exchange + '.txt') as f:
            pairs = [ type + '-' + line.strip() for line in f]
            #pairs.sort()
        f.close()

        # CHANGE CONFIG HERE!!! binance | bittrex
        if exchange == 'binance':
            port = 5000
        elif exchange == 'bittrex':
            port = 6000

        number_bot = read_config(exchange, 'number_bot')

        pairs_per_file = math.ceil(len(pairs)/number_bot)
        
        begin = 0
        content = ''
        content_linux = ''
        all_contents = ''
        all_contents_linux = ''
        strategies = ''

        for i in range(1, number_bot + 1):
            with open('template_' + exchange + '.js', 'r') as f:
                data = json.load(f)
            f.close()
            for j in range(begin, begin + int(pairs_per_file)):
                try:
                    #print(str(j+1) + '-' * 23 + '\n' + ' '*3 + exchange.capitalize() + ' > ' + pairs[j])
                    strategies = read_config(exchange, 'strategies')
                    #print(strategies)
                    data['pairs'][exchange][pairs[j]] = { 
                                                        "strategy": strategies, 
                                                        "override": {}      
                                    }
                    data['ws']['port'] = port + i
                except:
                    pass
                #Save to file
                with open('configs_'+ exchange + '/config' + str(i) + '_' + exchange + '.js', 'w', encoding='utf8') as f:
                    json.dump(data, f, indent=4)
                f.close()

                #Create Batch file for each bot
                content = 'start gunthy.exe --config=configs_' + exchange + '/config' + str(i) + '_' + exchange + '.js'
                content_linux = './gunthy-linx64 --config=configs_' + exchange + '/config' + str(i) + '_' + exchange + '.js'

            begin = begin + pairs_per_file
            all_contents += content + "\ntimeout 5\n"
            all_contents_linux += content_linux + " & \n"            
            if pairs_per_file * i > len(pairs):
                break
            
        #Create Batch file to RUN ALL
        with open('0_RunALL_GB' + '_' + exchange + '.bat', 'w', encoding='utf8') as f:
            f.write(all_contents)
        f.close()

        #Create Run file for LINUX
        with open('0_Linux_GB' + '_' + exchange, 'w', encoding='utf8') as f:
            f.write(all_contents_linux)
        f.close()        

    

if __name__ == "__main__":

    if not os.path.exists('configs_binance'):
        os.makedirs('configs_binance')
    if not os.path.exists('configs_bittrex'):
        os.makedirs('configs_bittrex')

    list_coins_bittrex(read_config('bittrex', 'key', 1), read_config('bittrex', 'secret', 1), read_config('bittrex', 'type'))
    
    list_coins_binance(read_config('binance', 'key', 1), read_config('binance', 'secret', 1), read_config('binance', 'type'))
