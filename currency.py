import requests 
from bs4 import BeautifulSoup 
import time 
import smtplib 


class Currency:
	# Лінк на на потрібну сторінку
	DOLLAR_UAH = 'https://www.google.com/search?q=usd+to+uah&oq=usd+to&aqs=edge.0.0i433i512l3j69i57j0i512l5.8065j0j9&sourceid=chrome&ie=UTF-8'
	# Заголовки для передачі разом з URL
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47'}

	current_converted_price = 0
	difference = 1 # Різниця після якої буде відправлено повідомлення на пошту

	def __init__(self):
		# Встановлення курсу валюти при створенні об'єкта
		self.current_converted_price = float(self.get_currency_price().replace(",", "."))

	# Метод для отримання курсу валюти
	def get_currency_price(self):
		# Парсим всю сторінку
		full_page = requests.get(self.DOLLAR_UAH, headers=self.headers)

		# Розбираємо через BeautifulSoup
		soup = BeautifulSoup(full_page.content, 'html.parser')

		# Отримуємо потрібне для нас значення и повертаємо його
		convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
		return convert[0].text

	# Перевірка зміни курсу
	def check_currency(self):
		currency = float(self.get_currency_price().replace(",", "."))
		if currency >= self.current_converted_price + self.difference:
			print("Курс сильно вырос, может пора что-то делать?")
			self.send_mail()
		elif currency <= self.current_converted_price - self.difference:
			print("Курс сильно упал, может пора что-то делать?")
			self.send_mail()

		print("Зараз курс: 1 USD = " + str(currency))
		time.sleep(3) # Засипання програми на 3 сек
		self.check_currency()

	# Відправка мейла через SMTP
	def send_mail(self):
		server = smtplib.SMTP('smtp.ukr.net', 465)
		server.ehlo()
		server.starttls()
		server.ehlo()

		server.login('MAIL', 'PASSWORD')

		subject = 'Currency mail'
		body = 'Currency has been changed!' 
		message = f'Subject: {subject}\n{body}'

		server.sendmail(
			'SENDER',
			'RECEIVER',
			message
		)
		server.quit()

currency = Currency()
currency.check_currency()
