#!/usr/bin/env python -W ignore::DeprecationWarning

import subprocess, selenium, requests, logging, base64, json, time, os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from termcolor import cprint
from zipfile import *
from sys import exit


class main:
	def __init__(self):
		logging.basicConfig(filename="errors.txt", level=logging.DEBUG)
		self.crashPoints = None
		self.multiplier = 0
		os.system("")
		try:
			self.getConfig()
			self.sendBet()
			self.sendMessages()
		except KeyboardInterrupt:
			self.print("Exiting program.")
			self.browser.close()
			exit()
		except Exception as e:
			open("errors.txt", "w+").close()
			now = time.localtime()
			logging.exception(f'A error has occured at {time.strftime("%H:%M:%S %I", now)}')
			self.print("An error has occured check logs.txt for more info", "error")
			time.sleep(2)
			raise
			self.browser.close()
			exit()

	def print(self, message="", option=None): # print the ui's text with
		print("[ ", end="")
		if not option:
			cprint("AUTOBET", "magenta", end="")
			print(" ] ", end="")
			if message:
			  cprint(message, "magenta")
		elif option == "error":
			cprint("ERROR", "red", end="")
			print(" ] ", end="")
			if message:
			  cprint(message, "red")
		elif option == "warning":
			cprint("WARNING", "yellow", end="")
			print(" ] ", end="")
			if message:
			  cprint(message, "yellow")
		elif option == "good":
			cprint("AUTOBET", "green", end="")
			print(" ] ", end="")
			if message:
			  cprint(message, "green")
		elif option == "bad":
			cprint("AUTOBET", "red", end="")
			print(" ] ", end="")
			if message:
			  cprint(message, "red")


	def clear(self): # Clear the console
		if os.name == 'nt':
		  os.system("cls")
		else:
		  os.system("clear")


	def getConfig(self): # Get configuration from data.json file
		uiprint = self.print
		print("[", end="")
		cprint(base64.b64decode(b'IENSRURJVFMg').decode('utf-8'), "cyan", end="")
		print("]", end="")
		print(base64.b64decode(b'TWFkZSBieSBKb3NoIzYzODI=').decode('utf-8'))
		time.sleep(3)
		self.clear()

		try:
			open("data.json", "r").close()
		except:
			uiprint("data.json file is missing. Make sure you downloaded all the files and they're all in the same folder", "error")

		with open("config.json", "r+") as data:

			config = json.load(data)
			try:
				self.auth = config["authorization"]
			except:
				print("1")
				uiprint("Invalid authorization inside JSON file. Enter your new authorization from BloxFlip", "error")
				time.sleep(1.6)
				exit()

			try:
				self.message = config["message"]
			except:
				print("1")
				uiprint("Invalid message inside JSON file. Must be valid string", "error")
				time.sleep(1.6)
				exit()


			latest_version = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE").text
			download = requests.get(f"https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_win32.zip")


			uiprint("Installing newest chrome driver...", "warning")
			subprocess.call('taskkill /im "chromedriver.exe" /f')
			os.chmod('chromedriver.exe', 0o777)
			os.remove("chromedriver.exe")


			with open("chromedriver.zip", "wb") as zip:
				zip.write(download.content)


			with ZipFile("chromedriver.zip", "r") as zip:
				zip.extract("chromedriver.exe")
			os.remove("chromedriver.zip")
			uiprint("Chrome driver installed.", "good")


			options = webdriver.ChromeOptions()
			options.add_experimental_option('excludeSwitches', ['enable-logging'])
			self.browser = webdriver.Chrome("chromedriver.exe", chrome_options=options)
			browser = self.browser
			browser.get("https://bloxflip.com/crash") # Open bloxflip
			browser.execute_script(f'''localStorage.setItem("_DO_NOT_SHARE_BLOXFLIP_TOKEN", "{self.auth}")''') # Login with authorization
			browser.execute_script(f'''window.location = window.location''')
			time.sleep(1.5)


			elements = browser.find_elements_by_css_selector('.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')
			if not elements:
				uiprint("Blocked by DDoS protection. Solve the captcha on the chrome window to continue.")
			while not elements:
				elements = browser.find_elements_by_css_selector('.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')


			try:
				balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss227.jss44").text.replace(',', ''))
			except selenium.common.exceptions.NoSuchElementException:
				try:
					balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss220.jss44").text.replace(',', ''))
				except selenium.common.exceptions.NoSuchElementException:
					try:
						balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss102.jss44").text.replace(',', ''))
					except selenium.common.exceptions.NoSuchElementException:
						uiprint("Invalid authorization. Make sure you copied it correctly, and for more info check the github", "bad")
						time.sleep(1.7)
						browser.close()
						exit()


	def ChrashPoints(self):		
		browser = webdriver.Chrome('chromedriver.exe')
		browser.get("https://rest-bf.blox.land/games/crash")

		history = None
		uiprint = self.print
		sent = False
		
		while True:
			browser.refresh()
			data = browser.page_source.replace('<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', "").replace("</pre></body></html>", "")
			try:
				games = json.loads(data)
			except json.decoder.JSONDecodeError:
				uiprint("Blocked by ddos protection. Solve the captcha to continue.", "error")
				time.sleep(20)
				browser.close()
				exit()
			if games["current"]["status"] == 2 and not sent:
				sent = True
				previd = games["current"]["_id"]
				yield ["game_start", games["history"][0]["crashPoint"]]
			elif games["current"]["status"] == 3:
				sent = False
			if not history == games["history"]:
				history = games["history"]
				yield ["history", [float(crashpoint["crashPoint"]) for crashpoint in history ]]
			time.sleep(0.01)

	def updateBetAmount(self, amount):
		browser = self.browser
		elemnts = browser.find_elements_by_css_selector('.MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedStart.MuiFilledInput-inputAdornedStart')
		for _ in range(10):
			elemnts[0].send_keys(f"{Keys.BACKSPACE}")
		elemnts[0].send_keys(f"{amount}")

	def sendBet(self): # Actually compare the user's chances of winning and place the bets
		uiprint = self.print
		uiprint("Nuking started.. Press Ctrl + C to exit")

		winning = 0
		losing = 0


		for game in self.ChrashPoints():
			if game[0] == "history":
				games = game[1]
				avg = sum(games)/len(games)
				uiprint(f"Average Crashpoint: {avg}")

			if game[0] == "game_start":
				uiprint("Game Starting...")
				try:
					balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss227.jss44").text.replace(',', ''))
				except selenium.common.exceptions.NoSuchElementException:
					try:
						balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss220.jss44").text.replace(',', ''))
					except selenium.common.exceptions.NoSuchElementException:
						try:
							balance = float(browser.find_element_by_css_selector(".MuiBox-root.jss102.jss44").text.replace(',', ''))
						except selenium.common.exceptions.NoSuchElementException:
							uiprint("Invalid authorization. Make sure you copied it correctly, and for more info check the github", "bad")
							time.sleep(1.7)
							browser.close()
							exit()
				uiprint(f"Draining robux.")
				self.updateBetAmount(balance)
				browser.find_element_by_css_selector(".MuiButtonBase-root.MuiButton-root.MuiButton-contained.jss142.MuiButton-containedPrimary").click()
				uiprint("Robux drained", "good")

	def sendMessages(self):
		browser = self.browser
		browser.find_element_by_css_selector(".MuiInputBase-input.MuiFilledInput-input").send_keys(self.message)
		while True:
			browser.find_element_by_css_selector("MuiButtonBase-root MuiButton-root jss34 MuiButton-contained").click()
			time.sleep(3)
if __name__ == "__main__":
	main()
