def pesquisar(termo, numbusca, qttd):
    import requests
    from bs4 import BeautifulSoup
    import json
    import re

    #1 - Relevância
    #2 - Data de lançamento (DESC)
    #3 - Nome (Alfabetico)
    #4 - Menor Preço
    #5 - Maior Preço
    #6 - Análises de úsuarios

    numbusca = int(numbusca)

    if numbusca == 1:
        tipobusca = ''
    elif numbusca == 2:
        tipobusca = 'Released_DESC'
    elif numbusca == 3:
        tipobusca = 'Name_ASC'
    elif numbusca == 4:
        tipobusca = 'Price_ASC'
    elif numbusca == 5:
        tipobusca = 'Price_DESC'
    elif numbusca == 6:
        tipobusca = 'Reviews_DESC'

    busca = termo.replace(' ', '%20')

    url = f'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by={tipobusca}&term={busca}&force_infinite=1&category1=998&snr=1_7_7_151_7&infinite=1'


    #pega o atributo total_count da url informada
    def totalresults(url):
        r = requests.get(url)
        data = dict(r.json())
        totalresults = data['total_count']
        return int(totalresults)

    #pega todo os dados da url como um json e os coloca dentro de um dicionario
    # e retorna este dicionario
    def get_data(url):
        r = requests.get(url)
        data = dict(r.json())
        return data['results_html']

    #pega dados do hover com base no id do item
    def get_hover_data(id):

        url = f'https://store.steampowered.com/apphoverpublic/{id}?review_score_preference=0&l=brazilian&pagev6=true'
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')

        try:
            reviews_raw = soup.find('div', class_='hover_review_summary').text
        except:
            reviews = 0

        else:
            pattern = r'\d+'
            reviews = int(''.join(re.findall(pattern, reviews_raw)))

        return reviews

    def parse(data):

        gameslist = []
        soup = BeautifulSoup(data, 'html.parser')
        games = soup.find_all('a')
        for game in games:
            title = game.find('span', {'class': 'title'}).text
            
            try:
                price = float(game.find('div', {'class': 'search_price'}).text.strip().split('R$')[-1].replace(',','.'))
                
            except:
                price = float(0)
            
            imgsrc = game.find('div', {'class': 'search_capsule'}).img['src']
            href = game['href']
            gameid = href.split('/')[4]
            
        
            released = game.find('div', class_='col search_released responsive_secondrow').text.split(':')[-1].strip()

            reviews = get_hover_data(gameid)

            mygame = {
                    'title': title,
                    'price': price,
                    'gameid': gameid,
                    'released': released,
                    'reviews': reviews,
                    'img': imgsrc,
                    'href': href,
            }
            gameslist.append(mygame)

        return gameslist

    results = []

    # quantidade de itens que serão pegos
    # para pegar todos utilizar a função totalresults com o url

    qttd = int(qttd)

    for x in range(0, qttd, 50):
        data = get_data(f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by={tipobusca}&term={busca}&snr=1_7_7_151_7&category1=998&infinite=1')
        results.append(parse(data))

    return results


if __name__ == ('__main__'):

    nome_jogo = 'Total War'

    tipo_busca = 1

    #1 - Relevância
    #2 - Data de lançamento (DESC)
    #3 - Nome (Alfabetico)
    #4 - Menor Preço
    #5 - Maior Preço
    #6 - Análises de úsuarios

    pesquisar(nome_jogo,tipo_busca,50)