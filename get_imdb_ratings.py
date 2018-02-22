import re
import sys
import urllib2
import urllib
from bs4 import BeautifulSoup

def get_movie_rating(name, movie_identifier):
  print "Scrapping from IMDB .... Will be back with your movie rating in a while .... "
  movie_url = "https://www.imdb.com/{0}".format(movie_identifier)
  soup = BeautifulSoup(urllib2.urlopen(movie_url), "html.parser")
  rating = soup.find(attrs={"itemprop": "ratingValue"})
  if rating is None:
    print "Sorry {} is not yet famous in IMDB. We can get rating only for 5 reviews.\n".format(name)
    sys.exit()
  print "{} IMDB Rating: {}".format(name, rating.text)

def get_soup(url):
	return BeautifulSoup(urllib2.urlopen(url), "html.parser")

def get_int(string_val):
  try:
    return int(string_val)
  except ValueError:
    return 0

def get_selection_from(op_text):
  user_input = raw_input(op_text)
  if(user_input == "Exit"):
    sys.exit()
  selection = get_int(user_input)
  if(selection > 0 and selection <= len(movie_links)):
    return int(selection)
  else:
    print "Please enter a valid value. (Eg. 1..{})\n".format(len(movie_links))
    return get_selection_from(op_text)

movie_name = sys.argv[1]
search_url = "https://www.imdb.com/find?q=" + urllib.quote_plus(movie_name)
movie_links = get_soup(search_url).find_all("a", href=re.compile("title"), text=re.compile("(?i)" + movie_name))
suggested_movies_count = len(movie_links)

if(suggested_movies_count > 1):
  print("We have got TOP suggestions based on your input. Please enter your Movie's option. \n\nP.S If you can't find the movie we are really sorry about that, type 'Exit' in that case.\n")
  selection = 0
  op_text = ""
  for index, movie_link in enumerate(movie_links):
    op_text += "{} - {}\n".format(index + 1, movie_link.parent.text)
  selected_link = movie_links[get_selection_from(op_text) - 1]
  get_movie_rating(selected_link.parent.text, selected_link.get("href"))
elif(suggested_movies_count == 1):
    get_movie_rating(movie_links[0].parent.text, movie_links[0].get("href"))
else:
  print "Sorry the entered movie's rating can't be found currently. Please feel free to use the system with other movies"