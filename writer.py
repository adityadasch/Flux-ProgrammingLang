line = 0

def write(data):
    with open('inter.txt', 'a') as f:
        global line
        line+=1
        f.write(f'{line:04} '+data+'\n')

close = lambda: 1