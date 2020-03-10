import urllib3, re, string, json, html
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib3.exceptions import HTTPError
from io import StringIO
from nltk.stem import PorterStemmer
import json

#TODO: Change the name of the collection DocitionaryEntry to News
from fnp.models import Article


class FetchData():
    englishDictionary = {}
    url = ''
    pageData = None
    err = None
    bsoup = None
    msgOutput = True
    extractedText = ''

    def init(self):
        with open('./fnp/modules/files/words_dictionary.json') as json_file:
            self.englishDictionary = json.load(json_file)


    def load_real_url(self, url):
        self.url = url

        httpmatch = re.compile(
            '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
        user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

        # Initiate PorterStemmer
        st = PorterStemmer()

        if httpmatch.match(self.url):
            try:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                http = urllib3.PoolManager(2, headers=user_agent)
                response = http.request('GET', self.url, timeout=urllib3.Timeout(connect=2.0))
                self.pageData = response.data
            except:
                self.err = {'message': "Error on HTTP request"}
                print(self.err)
                return False

        if self.pageData is None:
            print("No page data")
            return False

        self.bsoup = BeautifulSoup(self.pageData, 'html.parser')
        d_body = self.bsoup.findAll(text=True)
        viz_text = filter(self.is_visible, d_body)
        allVizText = " ".join(filter(self.is_visible, viz_text)).replace("\r\n", "").replace("\n", "") \
            .replace("\t", "")

        for elem in allVizText.split():
            reformatted = elem.lower()
            reformatted = reformatted.translate(str.maketrans('', '', string.punctuation))
            reformatted = reformatted.strip(string.punctuation)

            if reformatted in self.englishDictionary:
                reformatted = st.stem(reformatted)
                self.extractedText = self.extractedText + reformatted + " "

        return True

    def load_url(self, url, q_class):
        self.url = url

        httpmatch = re.compile('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
        user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

        # Initiate PorterStemmer
        st = PorterStemmer()

        if httpmatch.match(self.url):
            try:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                http = urllib3.PoolManager(2, headers=user_agent)
                response = http.request('GET', self.url, timeout=urllib3.Timeout(connect=2.0))
                self.pageData = response.data
            except:
                self.err = {'message': "Error on HTTP request"}
                print(self.err)
                return False

        if self.pageData is None:
            return False

        self.bsoup = BeautifulSoup(self.pageData, 'html.parser')
        d_body = self.bsoup.findAll(text=True)
        viz_text = filter(self.is_visible, d_body)
        allVizText = " ".join(filter(self.is_visible, viz_text)).replace("\r\n", "").replace("\n", "")\
            .replace("\t", "")

        for elem in allVizText.split():
            reformatted = elem.lower()
            reformatted = reformatted.translate(str.maketrans('', '', string.punctuation))
            reformatted = reformatted.strip(string.punctuation)

            if reformatted in self.englishDictionary:
                reformatted = st.stem(reformatted)
                self.extractedText = self.extractedText + reformatted + " "

        try:
            print(self.url)
            de = Article(body_text=self.extractedText, label=q_class, url=self.url)
            de.save()
        except:
            print("ERROR: Data didn't saved into database.")
            return False

        print("Data saved.")

        return True

    def is_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True


