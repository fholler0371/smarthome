import os

def menu(data):
    while True:
        os.system('clear')
        print('')
        if 'titel' in data:
            print(data['titel'])
            print('=' * len(data['titel']))
            print('')
        if 'entries' in data:
            l = 1
            for x in data['entries']:
                line = ''
                if l < 10:
                    line += ' '
                line += str(l)+'. '+x
                print(line)
                l += 1
        if 'entries2' in data:
            l = 1
            for x in data['entries2']:
                line = ''
                if l < 10:
                    line += ' '
                line += str(l)+'. '+x['label']
                print(line)
                l += 1
        print('')
        print(' x: '+data['exit'])
        print('')
        selection = input('Bitte eine Auswahl treffen:')
        if selection == "x":
            return -1
        else:
            try:
                ret = int(selection)
                if ret < l:
                    if 'entries2' in data:
                        ret = data['entries2'][ret-1]['cmd']
                    return ret
            except:
                pass
