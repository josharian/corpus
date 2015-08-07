#!/usr/bin/env python

import os
import subprocess
import sys

import progressbar
import requests
from bs4 import BeautifulSoup


class Item(progressbar.Widget):

    __slots__ = ('items',)

    def __init__(self, items):
        self.items = items

    def update(self, pbar):
    	if pbar.finished:
    		return "<done>"
        return self.items[pbar.currval]


def godoc_index():
	return requests.get('https://godoc.org/-/index').text


def main():
	print("Downloading godoc index")
	html = godoc_index()

	print("Parsing html")
	soup = BeautifulSoup(html)
	# import codecs
	# with codecs.open("index.html", 'r', 'utf-8') as f:
	# 	html = f.read()
	# 	soup = BeautifulSoup(html)

	print("Extracting package paths")
	pkgs = []
	for a in soup.select("tr > td > a"):
		pkgs.append(a.get_text().replace(u'\u200b', '').encode("utf-8"))

	print("Found ", len(pkgs), " packages")

	cwd = os.getcwd()
	env = os.environ
	env["GOPATH"] = cwd
	env["GIT_ASKPASS"] = "/bin/echo"

	widgets = [Item(pkgs), "   (", progressbar.Percentage(), ")   ", progressbar.widgets.Timer(), "   ", progressbar.widgets.ETA()]
	bar = progressbar.ProgressBar(widgets=widgets, maxval=len(pkgs)).start()

	for i, pkg in enumerate(pkgs):
		bar.update(i)
		p = subprocess.Popen(["go", "get", "-d", pkg], env=env)
		p.wait()
	bar.finish()

	return 0

if __name__ == "__main__":
	sys.exit(main())
