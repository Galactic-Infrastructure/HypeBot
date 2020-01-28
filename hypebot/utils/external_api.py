import json
import re
import requests
import string
import threading
import urllib
from bs4 import BeautifulSoup


ONELOOK_URL = 'https://api.datamuse.com/words?{params}'
GUBALLA_URL = 'https://www.guballa.de/vigenere-solver'
MW_URL = 'https://merriam-webster.com/thesaurus/{word}'
NUTRIMATIC_URL = 'https://nutrimatic.org/?q={content}'
QAT_URL = 'https://www.quinapalus.com/cgi-bin/qat?pat={pattern}&ent=Search&dict=0'
QQ_URL = 'https://6n9n93nlr5.execute-api.us-east-1.amazonaws.com/prod/solve'
REGEX_URL = 'http://thewordsword.com/regexp.php?{params}'
WOLFRAM_URL = 'https://www.wolframalpha.com/input/?'
WOLFRAM_API_URL = 'http://api.wolframalpha.com/v2/query?'
WORDPLAYS_URL = 'https://www.wordplays.com/crossword-solver/{params}'

USER_AGENT = ('Mozilla/5.0 (Windows NT 6.3; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36')


def onelook(pattern, top_n=20):
    defn = None
    if ':' in pattern:
        split = pattern.split(':')
        letters = split[0]
        defn = split[1]
    else:
        letters = pattern

    params = {}
    if letters:
        params['sp'] = letters
    if defn:
        params['ml'] = defn

    url_params = '&'.join([f'{k}={urllib.parse.quote(params[k])}' for k in params.keys()])
    url = ONELOOK_URL.format(params=url_params)

    response = requests.get(url)
    return url, [k['word'] for k in json.loads(response.content)[:top_n]]


def nutrimatic(content, top_n=20):
    url = NUTRIMATIC_URL.format(content=urllib.parse.quote(content))
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = [k.text for k in soup.find_all('span')]

    return url, results[:top_n]


def qat(pattern, top_n=30):
    url = QAT_URL.format(pattern=urllib.parse.quote(pattern))
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    if soup.select('div.in > table'):
        words = []
        for fragment in soup.select('div.in > table tr'):
            words.append(' '.join([td.text.strip() for td in fragment.select('td')]))
        return url, {0: words}
            
    d = {}
    countdown = -1
    for fragment in soup.select_one('div.in').contents:
        text_fragment = str(fragment)
        if 'Length' in text_fragment:
            key = int(re.sub('<.+>?', '', text_fragment.split(' ')[1]))
            countdown = 2
        else:
            if countdown >= 0:
                countdown -= 1
                if countdown == 0:
                    words = text_fragment.strip().split(' ')
                    d[key] = words

    return url, d


def regex(pattern, dictionary, case_sensitive=False):
    params = {
        'pattern': pattern,
        'dictname': dictionary,
        'casesensitive': 'True' if case_sensitive else 'False',
    }
    url_params = '&'.join([f'{k}={urllib.parse.quote(params[k])}' for k in params.keys()])
    url = REGEX_URL.format(params=url_params)
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    words = []

    for fragment in soup.select('div.odd, div.even'):
        text = fragment.text.strip()
        words.append(text)
            
    return 'http://thewordsword.com', words


def crossword(clue):
    encoded_clue = urllib.parse.quote(clue.replace(' ', '-'))

    url = WORDPLAYS_URL.format(params=encoded_clue)
    response = requests.get(url, headers={
        'user-agent': USER_AGENT,
    })

    soup = BeautifulSoup(response.content, 'html.parser')
    results = []

    for tr in soup.select('#adwrap-table tr.odd, #adwrap-table tr.even'):
        tds = tr.select('td')
        num_stars = len(tds[0].select('.stars div'))
        clue_answer = tds[1].text
        clue_text = tds[2].text
        results.append((num_stars, clue_answer, clue_text))

    return url, results


def fetch_thesaurus_list(word, selector):
    response = requests.get(
        MW_URL.format(word=word)
    )

    syn_list = []
    soup = BeautifulSoup(response.content, 'html.parser')
    for fragment in soup.select(selector):
        syn_list.append(fragment.text)

    return syn_list


def synonyms(word):
    return fetch_thesaurus_list(word, 'span.syn-list div.synonyms_list li a')


def antonyms(word):
    return fetch_thesaurus_list(word, 'span.ant-list div.synonyms_list li a')


def solve_cryptogram(message, top_n=8):
    # Queries quipqiup to solve cryptograms.
    # The details of the method used here are identical to those used on the quipqiup website.

    def _threaded_qq_request(url, data, responses):
        url_response = requests.post(url, data=data)
        formatted_responses = json.loads(url_response.content)['solutions']
        for r in formatted_responses:
            responses.append(r)

    threads = []
    responses = []
    for t in [0.5, 1.0, 2.0, 3.0, 4.0]:
        data = json.dumps({
            'ciphertext': message,
            'solve-spaces': ' ' not in message,
            'time': 4
        })
        thread = threading.Thread(target=_threaded_qq_request, args=(QQ_URL, data, responses))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    tmp_responses = sorted(responses, key=lambda k: -k['logp'])
    responses = []
    response_keys = set()
    for r in tmp_responses:
        if r['plaintext'] not in response_keys:
            responses.append(r)
            response_keys.add(r['plaintext'])

    responses = responses[:top_n]
    return responses 


def solve_vigenere(message):
    response = requests.get(GUBALLA_URL)
    session_id = response.cookies['PHPSESSID']
    soup = BeautifulSoup(response.content, 'html.parser')
    request_token = soup.select_one('input[name="REQUEST_TOKEN"]').attrs['value']

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'cache-control': 'max-age=0',
        'cookie': f'PHPSESSID={session_id}',
        'user-agent': USER_AGENT,
    }
    data = {
        'REQUEST_TOKEN': request_token,
        'cipher': message,
        'variant': 'vigenere',
        'lang': 'en',
        'key_len': '3-50',
        'break': 'Break Cipher',
    }

    response = requests.post(GUBALLA_URL, headers=headers, data=data)

    soup = BeautifulSoup(response.content, 'html.parser')

    key_text = soup.select_one('.vig_inner p').getText()

    key = key_text.split('"')[1]
    decoded = soup.select_one('textarea[name="clear_text"]').getText()

    return key, decoded


def wolfram_alpha(message):
    params = {
        'appid': 'U7VRR6-3X374V78YJ',
        'format': 'plaintext',
        'input': message,
    }
    response = requests.get(WOLFRAM_API_URL, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    out = ['<' + WOLFRAM_URL + urllib.parse.urlencode({'i': message}) + '>\n']
    for node in soup.descendants:
        if node.name == 'pod':
            out.append('**' + node.attrs['title'] + ':**\n')
        if node.name == 'plaintext':
            text = node.getText()
            if text.strip():
                out.append('```' + text.strip('\n') + '```')
        if node.name == 'didyoumean':
            out.append('Did you mean: *' + node.getText() + '*\n')
        if node.name == 'imagesource':
            out.append('<' + node.getText() + '>\n')
    return out
