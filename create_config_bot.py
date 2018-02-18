import json, math


for exchange in ('bittrex', 'binance'):
    #Select pairs
    pairs = []
    with open('pairs_choice_' + exchange + '.txt') as f:
        pairs = ['BTC-' + line.strip() for line in f]
        pairs.sort()
    f.close()

    # CHANGE CONFIG HERE!!! binance | bittrex
    if exchange == 'binance':
        port = 5000
        number_bot = 5
    elif exchange == 'bittrex':
        port = 5010
        number_bot = 10

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
            #with open(str(i) + '_GB' + '_' + exchange + '.bat', 'w', encoding='utf8') as f:
            #    f.write(content)
            #f.close()
        begin = begin + pairs_per_file
        all_contents += content + "\ntimeout 5\n"
        if pairs_per_file * i > len(pairs):
            break
        
    #Create Batch file to RUN ALL
    with open('0_RunALL_GB' + '_' + exchange + '.bat', 'w', encoding='utf8') as f:
        f.write(all_contents)
    f.close()
