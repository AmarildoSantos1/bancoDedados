import requests, csv
from bs4 import BeautifulSoup


def get_url(url: str, headers):
    try:
        # headers = {'Accept': self.accept}
        result = requests.get(url=url, headers=headers)
        return result
    except Exception as e:
        print(e)


def execute_request():
    url = f'https://www.kabum.com.br/hardware/placa-de-video-vga'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'}

    retorno = get_url(url=url, headers=headers)
    old_product_price, new_price, product_name = '', '', ''

    soup = BeautifulSoup(retorno.content, 'html.parser')
    list_products = soup.find_all("div", class_="sc-d55b419d-7 bwqahi productCard")
    dict_products = {}

    for product in list_products:
        calc_discount = True
        soup_name = product.find_all("span", class_="sc-d79c9c3f-0 nlmfp sc-d55b419d-16 giuuaP nameCard")
        soup_price = product.find_all("div", class_="sc-3b515ca1-0 gyJsdF availablePricesCard")
        for i in soup_name: product_name = i.text

        for j in soup_price:
            new_price = j.contents[1].text
            old_product_price = j.contents[0].text
            if not len(old_product_price):
                old_product_price = new_price
                calc_discount = False

        old_product_price_ = ((old_product_price.replace('R$', '').strip()).replace('.', '')).replace(',', '.')
        new_price_ = (new_price.replace('R$', '').strip()).replace('.', '').replace(',', '.')
        if calc_discount:
            desconto = round(((float(old_product_price_) - float(new_price_)) / float(old_product_price_)) * 100)
        else: desconto = '0.0'

        dict_products[product_name] = {'old_price': f'R$ {old_product_price_}',
                                       'new_price': f'R$ {new_price_}',
                                       'discount': f'{desconto} %'}

    with open('dados_kabum', 'w', newline='') as arquivo_csv:
        fields = ["product_name", "old_price", "new_price", "discount"]
        escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=fields)
        escritor_csv.writeheader()

        for product_name, dados in dict_products.items():
            dados['product_name'] = product_name  # Adicione o nome do cliente como coluna extra
            escritor_csv.writerow(dados)

execute_request()