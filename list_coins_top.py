<<<<<<< HEAD
from bittrex import bittrex
from binance import Client
import operator, json, math

def read_config(exchange, param):
    with open('settings.json', 'r') as f:
        data = json.load(f)
    result = data[exchange][param]
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
        if float(balances['balances'][i]['free']) > 0.00000000:
            balance_coins.append(balances['balances'][i]['asset'])

    ###
    # Construct list of coins to trade with volume criteria
    ###
    for i in range(0, len(tableaux)):

        if type in tableaux[i]['symbol'] and 'USD' not in tableaux[i]['symbol']:
            data[tableaux[i]['symbol']] = tableaux[i]['quoteVolume']
            
    sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(int(read_config('bittrex', 'first_position')), int(read_config('bittrex', 'last_position'))):
        #print(sorted_data[i][0][4:] + '-----' + str(sorted_data[i][1]))
        contents.append(sorted_data[i][0][:-3])

    s_c_coins = set(contents)  
    s_b_coins = set(balance_coins)
 
    results = sorted(s_c_coins|s_b_coins) #union
    all_contents =''
    for result in results:
        all_contents += result + '\n'

    with open('Choices_Binance.txt', 'w', encoding='utf8') as f:
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
        if float(balances[i]['Available']) > 0.0:
            balance_coins.append(balances[i]['Currency'])

    ###
    # Construct list of coins to trade with volume criteria
    ###
    for i in range(0, len(tableaux)):

        if type in tableaux[i]['MarketName'] and 'USD' not in tableaux[i]['MarketName']:
            data[tableaux[i]['MarketName']] = tableaux[i]['BaseVolume']
            
    sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
    #print(sorted_data)

    for i in range(int(read_config('bittrex', 'first_position')), int(read_config('bittrex', 'last_position'))):
        #print(sorted_data[i][0][4:] + '-----' + str(sorted_data[i][1]))
        contents.append(sorted_data[i][0][4:])

    s_c_coins = set(contents)    
    s_b_coins = set(balance_coins)
    results = sorted(s_c_coins|s_b_coins) #union

    all_contents =''
    for result in results:
        all_contents += result + '\n'

    with open('Choices_Bittrex.txt', 'w', encoding='utf8') as f:
        f.write(all_contents)
    f.close()

    create_file_config(type)

def create_file_config(type): 
    for exchange in ('bittrex', 'binance'):
        #Select pairs
        pairs = []
        with open('Choices_' + exchange + '.txt') as f:
            pairs = [ type + '-' + line.strip() for line in f]
            pairs.sort()
        f.close()

        # CHANGE CONFIG HERE!!! binance | bittrex
        if exchange == 'binance':
            port = 5000
        elif exchange == 'bittrex':
            port = 5010

        number_bot = read_config(exchange, 'number_bot')

        pairs_per_file = math.ceil(len(pairs)/number_bot)
        begin = 0
        all_contents = ''

        for i in range(1, number_bot + 1):
            with open('template_' + exchange + '.js', 'r') as f:
                data = json.load(f)
            f.close()
            for j in range(begin, begin + int(pairs_per_file)):
                try:
                    print(str(j+1) + '-' * 23 + '\n' + ' '*3 + exchange.capitalize() + ' > ' + pairs[j])
                    
                    data['pairs'][exchange][pairs[j]] = { 
                                                        "strategy": "bbtssl", 
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

            begin = begin + pairs_per_file
            all_contents += content + "\ntimeout 5\n"
            if pairs_per_file * i > len(pairs):
                break
            
        #Create Batch file to RUN ALL
        with open('0_RunALL_GB' + '_' + exchange + '.bat', 'w', encoding='utf8') as f:
            f.write(all_contents)
        f.close()

    

if __name__ == "__main__":

    list_coins_bittrex(read_config('bittrex', 'key'), read_config('bittrex', 'secret'), read_config('bittrex', 'type'))
    
    list_coins_binance(read_config('binance', 'key'), read_config('binance', 'secret'), read_config('binance', 'type'))
=======
from bittrex import bittrex
from binance import Client
import operator, json, math

def read_config(exchange, param):
    with open('settings.json', 'r') as f:
        data = json.load(f)
    result = data[exchange][param]
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
        if float(balances['balances'][i]['free']) > 0.00000000:
            balance_coins.append(balances['balances'][i]['asset'])

    ###
    # Construct list of coins to trade with volume criteria
    ###
    for i in range(0, len(tableaux)):

        if type in tableaux[i]['symbol'] and 'USD' not in tableaux[i]['symbol']:
            data[tableaux[i]['symbol']] = tableaux[i]['quoteVolume']
            
    sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(int(read_config('bittrex', 'first_position')), int(read_config('bittrex', 'last_position'))):
        #print(sorted_data[i][0][4:] + '-----' + str(sorted_data[i][1]))
        contents.append(sorted_data[i][0][:-3])

    s_c_coins = set(contents)  
    s_b_coins = set(balance_coins)
 
    results = sorted(s_c_coins|s_b_coins) #union
    all_contents =''
    for result in results:
        all_contents += result + '\n'

    with open('Choices_Binance.txt', 'w', encoding='utf8') as f:
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
        if float(balances[i]['Available']) > 0.0:
            balance_coins.append(balances[i]['Currency'])

    ###
    # Construct list of coins to trade with volume criteria
    ###
    for i in range(0, len(tableaux)):

        if type in tableaux[i]['MarketName'] and 'USD' not in tableaux[i]['MarketName']:
            data[tableaux[i]['MarketName']] = tableaux[i]['BaseVolume']
            
    sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
    #print(sorted_data)

    for i in range(int(read_config('bittrex', 'first_position')), int(read_config('bittrex', 'last_position'))):
        #print(sorted_data[i][0][4:] + '-----' + str(sorted_data[i][1]))
        contents.append(sorted_data[i][0][4:])

    s_c_coins = set(contents)    
    s_b_coins = set(balance_coins)
    results = sorted(s_c_coins|s_b_coins) #union

    all_contents =''
    for result in results:
        all_contents += result + '\n'

    with open('Choices_Bittrex.txt', 'w', encoding='utf8') as f:
        f.write(all_contents)
    f.close()

    create_file_config(type)

def create_file_config(type): 
    for exchange in ('bittrex', 'binance'):
        #Select pairs
        pairs = []
        with open('Choices_' + exchange + '.txt') as f:
            pairs = [ type + '-' + line.strip() for line in f]
            pairs.sort()
        f.close()

        # CHANGE CONFIG HERE!!! binance | bittrex
        if exchange == 'binance':
            port = 5000
        elif exchange == 'bittrex':
            port = 5010

        number_bot = read_config(exchange, 'number_bot')

        pairs_per_file = math.ceil(len(pairs)/number_bot)
        begin = 0
        all_contents = ''

        for i in range(1, number_bot + 1):
            with open('template_' + exchange + '.js', 'r') as f:
                data = json.load(f)
            f.close()
            for j in range(begin, begin + int(pairs_per_file)):
                try:
                    print(str(j+1) + '-' * 23 + '\n' + ' '*3 + exchange.capitalize() + ' > ' + pairs[j])
                    
                    data['pairs'][exchange][pairs[j]] = { 
                                                        "strategy": "bbtssl", 
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

            begin = begin + pairs_per_file
            all_contents += content + "\ntimeout 5\n"
            if pairs_per_file * i > len(pairs):
                break
            
        #Create Batch file to RUN ALL
        with open('0_RunALL_GB' + '_' + exchange + '.bat', 'w', encoding='utf8') as f:
            f.write(all_contents)
        f.close()

    

if __name__ == "__main__":

    list_coins_bittrex(read_config('bittrex', 'key'), read_config('bittrex', 'secret'), read_config('bittrex', 'type'))
    
    list_coins_binance(read_config('binance', 'key'), read_config('binance', 'secret'), read_config('binance', 'type'))
>>>>>>> ae0203632e2a27c0b15e6d3ac6e8872ba16c359e
