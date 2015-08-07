pip install -r requirements.txt
python download.py

Why python? Because of BeautifulSoup.

TODO: That shit is outdated. If I actually read the frickin' page, I'd see that there
was an API for this:

http://api.godoc.org/packages

type Response struct {
	Results []struct {
		Path string `json:"path"`
	} `json:"results"`
}
