import requests
import pycountry


def Datas_colect(url):
    try:
        # a api abre e, quando nao for mais usada, fecha
        with requests.get(url) as answer:
            # vai pegar os dados que a api pegar e devolver em json
            answer.raise_for_status()
            return answer.json()

    # verifica se e um erro relacionado ao http
    except requests.exceptions.HTTPError as err:
        # verifica se o erro foi 404 (Not Found), ou seja, a cidade nao foi encontrada
        if err.response is not None and err.response.status_code == 404:
            print("\33[31mCity not found! Check your handwriting.\33[0m\n")
        else:
            print(f"\33[31mErro HTTP in API: {err}\33[0m\n")
            return None

    except Exception as err:
        # para erros de coneccao e qualquer outro que possivelmente possa dar
        print(f"\33[31mThere was a connection error: {err}\33[0m\n")
        # status 200 significa que ta OK e que a solicitação foi recebida, compreendida e processada com exito
        if 'answer' in locals() and answer.status_code != 200:
            print(f"\33[31mAPI details: {answer.text}\33[0m\n")


def API_enter(city,country):
    # define a chave  da api
    API_KEY = "41c1c03c0da0ab51e5353e8e0809c3f9"
    CITY = f"{city},{country}"
    # URL da API OpenWeatherMap
    url = f"https://api.openweathermap.org/data/2.5/weather?q={requests.utils.quote(CITY)}&appid={API_KEY}&units=metric&lang=in_us"

    # retorna a funcao da API
    return Datas_colect(url)


# pode usar com acento normalmente, mas nao precisa, tanto com city tanto com country
country = input("Enter the country (in English): \n").strip()
city = input("Enter a city: \n").strip()

# pega o codigo ISO 3166-1 alpha-2, ou seja, transforma 'brazil' em 'br', 'EUA' em 'us', etc
iso_code = pycountry.countries.lookup(country.title()).alpha_2
# chama a funcao base
data = API_enter(city, iso_code)

if data:
    # exemplo simples de uso dos dados
    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]
    print(f"Temperature in {city}, {country}: {temperature}°C ({description})\n")

input("Press Enter to exit...")