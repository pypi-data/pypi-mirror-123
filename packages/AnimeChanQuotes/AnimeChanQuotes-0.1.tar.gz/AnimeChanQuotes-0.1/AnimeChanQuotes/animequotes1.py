"""
Uses the anime quotes api to generate random and specific quotes
"""

import requests, sys, traceback

class AQ:

	def __init__(self, verbose=False, headers=None):
		self.base = "https://animechan.vercel.app/api/"
		self.rand = "random"
		self.tenrand = "quotes"
		self.bytitle = "quotes/anime" # params = title, page
		self.charname = "quotes/character" # params = name, page
		self.available = "available/anime"
		self.verbose = verbose # For debugging purposes.
		self.headers = headers # In case you want to run a custom header or user-agent.

		


	"""
	The following is url builder functions for the api.
	"""
	def get_base(self) -> str:

		return self.base

	def get_rand(self) -> str:

		return self.base + self.rand

	def get_tenrand(self) -> str:

		return self.base + self.tenrand

	def get_bytitle(self) -> str:

		return self.base + self.bytitle

	def get_charname(self) -> str:

		return self.base + self.charname

	def get_available(self) -> str:

		return self.base + self.available


	def is_string(self, q): #error handling for params. Checks if string.
		if isinstance(q, str):
			return True
		else:
			return False

	"""
	Request functions.
	"""
	def title_resp(self, query, page="1"):
		"""
		Used for random quotes by anime title. Limited selection of titles.
		query: str: Title of an available anime.
		page: str: it needs to be an integer in str format. This is checked.
		"""

		checkq = self.is_string(query) #checks if query and page are strings
		checkp = self.is_string(page)
		
		if checkq and checkp:

			
			t_param = {"title": query, "page": page} #parameters are built here
			t = self.get_bytitle()

			try:
				if self.headers: # applies custom headers. If self.headers is None it hits the else
					
					r = requests.get(t, params=t_param, headers = self.headers)
					r.raise_for_status()
					return r.json()
				else:
					
					r = requests.get(t, params=t_param)
					r.raise_for_status()
					return r.json()

			except Exception as e:
				if self.verbose:
					print("An exception has occurred with requests.")
					traceback.print_exception(*sys.exc_info())
					return
				else:
					return

		else:
			if self.verbose:
				print("One or both of your variables are not strings. Query: {} Page: {}".format(checkq, checkp))
				return

	def char_resp(self, query, page="1"):
		"""
		Used for random quotes by anime character. Limited selection of characters.
		query: str: Title of an available anime.
		page: str: it needs to be an integer in str format. This is checked
		"""
		checkq = self.is_string(query)#checks if query and page are strings
		checkp = self.is_string(page)

		if checkq and checkp:
			c = self.get_charname()
			c_param = {"name": query, "page": page} #parameters are built here.

			try:
				if self.headers:# applies custom headers. If self.headers is None it hits the else
					r = requests.get(c, params=c_param, headers = self.headers)
					r.raise_for_status()
					return r.json()
				else:
					r = requests.get(c, params=c_param)
					r.raise_for_status()
					return r.json()
				

			except Exception as e:
				if self.verbose:
					print("An exception has occurred with requests.")
					traceback.print_exception(*sys.exc_info())
					return
				else:
					return
		else:
			if self.verbose:
				print("One or both of your variables are not strings. Query: {} Page: {}".format(checkq, checkp))
				return
			else:
				return

	def resp(self, quant):
		"""
		Used to access the random quote, ten random quote and all anime
		api ends.
		quant: str: 'one', 'ten', or 'any' is the only acceptable variables.
		"""

		end = None

		if quant.lower() == "one": #checks for key strings. 
			end = self.get_rand()
		elif quant.lower() == "ten":
			end = self.get_tenrand()
		elif quant.lower() == "any":
			end= self.get_available()

		else:
			if self.verbose:
				print("Please supply the quant parameter. The only valid response is either 'one', 'ten' or 'any'. ")
				return
			else:
				return


		try:
			if self.headers:
				r = requests.get(end, headers = self.headers)
				r.raise_for_status()

				return r.json()
			else:
				r = requests.get(end)
				r.raise_for_status()
				
				return r.json()

		except Exception as e:
			if self.verbose:
				print("An exception has occurred with requests.")
				traceback.print_exception(*sys.exc_info())
				return
			else:
				return

if __name__ == "__main__":

	a = AQ(True)

	print("RANDOM QUOTE")
	u = a.resp("one")
	print(u)
	print("""

------------------------------------------------------------------------------------------------------------

		""")
	print("TEN RANDOM QUOTES")
	u = a.resp("ten")
	print(u)
	print("""

------------------------------------------------------------------------------------------------------------

		""")
	print("ALL AVAILABLE SERIES")
	u = a.resp("any")
	print(u)
	print("""

------------------------------------------------------------------------------------------------------------

		""")
	print("RANDOM BY TITLE: One Punch Man")
	u = a.title_resp("One Punch Man", "3")
	print(u)
	print("""

------------------------------------------------------------------------------------------------------------

		""")
	print("RANDOM BY CHARACTER: Saitama from One Punch Man")
	u = a.char_resp("saitama", "3")
	print(u)
