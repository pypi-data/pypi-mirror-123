import animequotes1

"""
The only class is AQ and it has 2 optional parameters. The first takes 
boolean for error checking "verbose" and the second is for custom headers "headers"
defaults for these are:
verbose = False
Headers = None
"""

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
print("""

------------------------------------------------------------------------------------------------------------

	""")
#Endpoint url builder functions for all your customized calling needs. Returns string

a.get_base()
a.get_tenrand()
a.get_rand()
a.get_bytitle()
a.get_charname()
a.get_available()


#the following uses isinstance() to check for strings. Returns boolean

a.is_string()