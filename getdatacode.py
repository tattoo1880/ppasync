from bs4 import BeautifulSoup



def get_datacode(code):
    result = ''
    with open('country.html','r')as f:
        result = f.read()
    
    soup = BeautifulSoup(result,'html.parser')
    options = soup.find_all('option')
    data = {}
    for op in options:
        data[op['data-code']] = op['value']
    with open('datacode.json','w')as f:
        f.write(str(data)) 
        
    # print(data)
    res = data.get('+'+code)
    #print('------------------------------',res)
    return res
        
        
        
if __name__ == '__main__':
    res = get_datacode('52')
    print(res)