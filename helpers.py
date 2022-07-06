from flask import redirect, render_template, request, session
from functools import wraps
import innertube
import json


def search_song(q):
	client = innertube.InnerTube("WEB")
	data = client.search(q)

	# Retrieve list of useful searches
	contents = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
	data = []

	# Loop through some portion of contents and collect info
	for i in range(len(contents)):
		
		try:
			videoContent = contents[i]['videoRenderer']
		except KeyError:
			break

		thumbnail = videoContent['thumbnail']['thumbnails']
		data.append({
			'id': videoContent['videoId'],
			# 'thumbnail': {
			# 	'url': thumbnail[0]['url'],
			# 	'width': thumbnail[0]['width'],
			# 	'height': thumbnail[0]['height']
			# },
			'thumbnail': thumbnail[0]['url'],
			'title': videoContent['title']['runs'][0]['text'],
			'channel': videoContent['ownerText']['runs'][0]['text']
			})

	return data


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function