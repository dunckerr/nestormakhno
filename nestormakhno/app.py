#https://twdown.net/?error=nolink
#https://cloudconvert.com/mov-to-mp4
from flask import Flask, render_template, request, send_from_directory

import os
import sys
import logging
import re

# https://twdown.net/download.php

WORDLEN = 5

if sys.platform == 'win32':
    app = Flask(__name__, static_folder="static")
    app.debug = True
else:
    app = Flask(__name__, static_url_path='/home/x1lcedpr5zdi/WebSite1', static_folder="static")


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# copy vars for global website
_disallowed = set()
_mask = '.....'
global _word5
_word5 = list()

def set_2_regex(s):
    r = '[^'
    for c in s:
        r = r + c
    r = r + ']'
    return r

def dk_input(prompt, default, maxlen):

    while True:
        logger.warning(prompt)
        r = input(prompt+'('+default+'):')
        if default is not None and r == '':
            return default
        elif len(r) == maxlen:
            return r
        else:
            pass

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

def gen_possibles(mask, nots):
    #print("got args mask {mask} nots {nots}")
    if len(nots) == 0:
        nots_bracket = "."
    else:
        nots_bracket = "[^"+nots+"]"
    newmask = ""
    for i in range(0,5):
        # TODO blank entry in form needs to be nadled here
        #print(f"processing {i} {mask} len {len(mask)}")
        if mask[i] == ".":
            newmask += nots_bracket
        else:
            newmask += mask[i]

    print("generated mask"+newmask)
    r = re.compile('^' + newmask + '$')
    fp = open('EN-UNIX-99171', 'r')
    wtmp = fp.read()
    words = wtmp.split('\n')
    word5 = list(filter(r.match, words))
    print('words list len '+str(len(words)))
    print('possibles list len '+str(len(word5)))

    return word5

def genmask(green,yellow,nots):
    if len(green) > 0:
        return green[0]
    else:
        if len(yellow) > 0:
            if len(nots) > 0:
                #return "[^"+yellow[0]+nots+"]"
                return "[^"+yellow+nots+"]"
            else:
                return "[^"+yellow+"]"
                #return "[^"+yellow[0]+"]"
        else:
            if len(nots) > 0:
                return "[^"+nots+"]"
            else:
                return "."

def getUserChar3(maxrow, col, ds, yellowGreen):
    found = ""
    if yellowGreen == "g":
        found = ds[0][col]  # green always row1
    else:
        for i in range(1,maxrow+1):
            print(f"testing {yellowGreen} row {i} col {col}")
            if len(ds[i][col]) > 0:
                found = found + ds[i][col]
                print(f"char added for {yellowGreen} row {i} col {col} is {found}")

    print(f"char for {yellowGreen} col {col} maxrow {maxrow} is {found}")
    return found

def getUserChar(maxrow, col, ds, yellowGreen):
    found = ""
    for i in range(0,maxrow+1):
        if len(ds[i][col]) > 0:
            if yellowGreen == "y":
                found = found + ds[i][col]
            else:
                found = ds[i][col]
            print(f"char for {yellowGreen} col {col} is {found}")

    return found

def new_gen(ds, nots):
    # start with top row 0 indexed
    maxrow = -1
    for c in range(0,5):
        for i in range(0,10):
            if len(ds[c][i]) > 0:
                print(f"FOUND DATA AT row {c} pos {i}")
                maxrow = c
    print(f"MAX ROW {maxrow}")
    g1 = getUserChar(maxrow, 0, ds, "g") # row 0 greens
    g2 = getUserChar(maxrow, 1, ds, "g") # row 1 greens
    g3 = getUserChar(maxrow, 2, ds, "g") # row 2 greens
    g4 = getUserChar(maxrow, 3, ds, "g") # row 3 greens
    g5 = getUserChar(maxrow, 4, ds, "g") # row 4 greens
    y1 = getUserChar(maxrow, 5, ds, "y") # row 0 yellows
    y2 = getUserChar(maxrow, 6, ds, "y") # row 1 yellows
    y3 = getUserChar(maxrow, 7, ds, "y") # row 2 yellows
    y4 = getUserChar(maxrow, 8, ds, "y") # row 3 yellows
    y5 = getUserChar(maxrow, 9, ds, "y") # row 4 yellows
    yellows = set(y1+y2+y3+y4+y5)

    words,mask = gen_possibles_extra(g1,g2,g3,g4,g5,y1,y2,y3,y4,y5,nots)

    # TODO remove words not in yellows
    words2 = list()
    for w in words:
        if containsAll(w, yellows):
            words2.append(w)

    return words2,mask

def new3_gen(ds, nots):
    # start with top row 0 indexed
    maxrow = -1
    for r in range(0,6):
        for c in range(0,5):
            if len(ds[r][c]) > 0:
                print(f"FOUND DATA AT row {r} pos {c}")
                maxrow = r
    print(f"MAX ROW {maxrow}")
    g1 = getUserChar3(maxrow, 0, ds, "g") # row 0 greens
    g2 = getUserChar3(maxrow, 1, ds, "g") # row 1 greens
    g3 = getUserChar3(maxrow, 2, ds, "g") # row 2 greens
    g4 = getUserChar3(maxrow, 3, ds, "g") # row 3 greens
    g5 = getUserChar3(maxrow, 4, ds, "g") # row 4 greens
    y1 = getUserChar3(maxrow, 0, ds, "y") # row 0 yellows
    y2 = getUserChar3(maxrow, 1, ds, "y") # row 1 yellows
    y3 = getUserChar3(maxrow, 2, ds, "y") # row 2 yellows
    y4 = getUserChar3(maxrow, 3, ds, "y") # row 3 yellows
    y5 = getUserChar3(maxrow, 4, ds, "y") # row 4 yellows
    yellows = set(y1+y2+y3+y4+y5)

    words,mask = gen_possibles_extra(g1,g2,g3,g4,g5,y1,y2,y3,y4,y5,nots)

    # TODO remove words not in yellows
    words2 = list()
    for w in words:
        if containsAll(w, yellows):
            words2.append(w)

    return words2,mask



def gen_possibles_extra(c1,c2,c3,c4,c5,y1,y2,y3,y4,y5,nots):
    newmask = ""
    newmask += genmask(c1,y1,nots)
    newmask += genmask(c2,y2,nots)
    newmask += genmask(c3,y3,nots)
    newmask += genmask(c4,y4,nots)
    newmask += genmask(c5,y5,nots)

    #print("generated mask:"+newmask)
    logger.warning("generated mask:"+newmask)
    r = re.compile('^' + newmask + '$')
    fp = open('lower-only', 'r')
    wtmp = fp.read()
    words = wtmp.split('\n')
    word5 = list(filter(r.match, words))

    return word5,newmask


def containsAll(str, cset):
    """
    :param str: check whether str contains ALL of the chars in cset
    :param cset:
    :return:
    """
    return 0 not in [c in str for c in cset]

def main_test():
    mask = '.....'
    r = re.compile('^'+mask+'$')
    fp = open('EN-UNIX-99171', 'r')
    wtmp = fp.read()
    words = wtmp.split('\n')
    word5 = list(filter(r.match, words))
    logger.warning('words list len '+str(len(words)))
    logger.warning(str(WORDLEN)+' letter words '+str(len(word5)))

    # these will come from url
    disallowed = set()
    while True:
        logger.warning('current mask '+mask)
        logger.warning('disallowed '+disallowed)

        mask = dk_input('mask:', mask, WORDLEN)
        ch = dk_input('bad char:', None, 1)
        disallowed.add(ch)

        # now were in business we have regex mask and disallowed
        # generate a regex
        r2 = '^'
        for i in range(0, 5):
            if mask[i] == '.':
                r2 = r2 + set_2_regex(disallowed)
            else:
                r2 = r2 + mask[i]

        r2 = r2 +'$'
        logger.warning('made regex '+r2)

        r3 = re.compile(r2)
        poss = list(filter(r3.match, word5))
        logger.warning('possibilities '+str(len(poss))+poss[0] + ' ' + poss[1])

def _init():
    _mask = '[A-Za-z][A-Za-z][A-Za-z][A-Za-z][A-Za-z]'
    r = re.compile('^'+_mask+'$')
    fp = open('EN-UNIX-99171', 'r')
    wtmp = fp.read()
    words = wtmp.split('\n')
    global _word5
    _word5 = list(filter(r.match, words))
    return '<H3>' + str(len(_word5)) + '</H3>'


HELP = '<H1>HELP v1.1<p>CASE SENSITIVE DICT. /words word count<p>/str 1par<p>/str/str mask/allowed<p>/init initialise words</H1>'

def dkrender(html, img):
    if sys.platform == 'win32':
        return render_template(html, user_image=img, path="\\static\\")
    else:
        return render_template(html, user_image=img, path="/home/x1lcedpr5zdi/WebSite1/")


#@app.route("/zz1")
#def show_indexz1():
    #return dkrender("index.html", "IMG_0021.jpg")

#@app.route("/zz2")
#def show_indexz2():
    #return dkrender("index2.html", "IMG_0021.jpg")

@app.route("/cat")
def show_cat():
    return dkrender("cat.html", "IMG_1820.mp4")


# use to get info to user from godaddy
@app.route("/pwd")
def show_index2():
    return os.getcwd()

@app.route("/nestor")
def nestor():
    return dkrender("main.html", "pic1.png")

@app.route("/")
def hello():
    return dkrender("new3.html", "pic1.png")
    #return dkrender("wordlcheat.html", "pic1.png")

@app.route("/words")
def test():
    global _word5
    return '<H2>len words ' + str(len(_word5)) + '</H2>'

@app.route("/session")
def test_session():
    global _word5
    return 'len session[words] ' + str(len(_word5))

@app.route("/init")
def init():
    #app.logger.error('app logging init called')
    return _init()


#@app.route("/<string:name>/")
#def say_hello(name):
    #return 'called with ' +name

# Load Browser Favorite Icon
#@app.route('/rb-star.ico')
#def favicon():
    #return url_for('static', filename='image/favicon.ico')


@app.route("/<string:mask>/<string:disallowed>")
def say_hello2(mask, disallowed):
    # now were in business we have regex mask and disallowed
    # generate a regex
    r2 = '^'
    for i in range(0, WORDLEN):
        if mask[i] == '.':
            r2 = r2 + set_2_regex(disallowed)
        else:
            r2 = r2 + mask[i]

    r2 = r2 + '$'

    r3 = re.compile(r2)
    poss = list(filter(r3.match, _word5))
    #if len(poss) < 30:
    return '<H3>' + str(poss[0: min(100, len(poss))]) + '</H3>'
    #else:
        #return '<H3>' + str(len(poss))+'/'+str(len(_word5)) + '</H3>'

#################  MAPPINGS ###################
# /wordlcheat  -> data.hmtl  ->  /data gen_possibles_extra   ALL WORKING
# /new  -> newword.html -> /data2
# /new3 -> new3.html -> /data3
@app.route('/wordlcheat')
def form():
    return render_template('wordlcheat.html')

@app.route('/new')
def form2():
    return render_template('newwordl.html')

@app.route('/new3')
def form3():
    return render_template('new3.html')

@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return "The URL /data is accessed directly. Try going to '/wordlcheat' to submit form"
    if request.method == 'POST':
        form_data = request.form
        words,mask = gen_possibles_extra(form_data['c1'], form_data['c2'], form_data['c3'], form_data['c4'], form_data['c5'], form_data['y1'], form_data['y2'], form_data['y3'], form_data['y4'], form_data['y5'], form_data['nn'])
        xlen=len(words)
        return render_template('data.html', form_data=form_data, words=words, xlen=xlen, mask=mask)

@app.route('/data2', methods=['POST', 'GET'])
def data2():
    if request.method == 'GET':
        return "The URL /data2 is accessed directly. Try going to '/new' to submit form"
    if request.method == 'POST':
        fd = request.form
        ds = [
            [fd['r1g1'], fd['r1g2'], fd['r1g3'], fd['r1g4'], fd['r1g5'], fd['r1y1'], fd['r1y2'], fd['r1y3'], fd['r1y4'], fd['r1y5']],
            [fd['r2g1'], fd['r2g2'], fd['r2g3'], fd['r2g4'], fd['r2g5'], fd['r2y1'], fd['r2y2'], fd['r2y3'], fd['r2y4'], fd['r2y5']],
            [fd['r3g1'], fd['r3g2'], fd['r3g3'], fd['r3g4'], fd['r3g5'], fd['r3y1'], fd['r3y2'], fd['r3y3'], fd['r3y4'], fd['r3y5']],
            [fd['r4g1'], fd['r4g2'], fd['r4g3'], fd['r4g4'], fd['r4g5'], fd['r4y1'], fd['r4y2'], fd['r4y3'], fd['r4y4'], fd['r4y5']],
            [fd['r5g1'], fd['r5g2'], fd['r5g3'], fd['r5g4'], fd['r5g5'], fd['r5y1'], fd['r5y2'], fd['r5y3'], fd['r5y4'], fd['r5y5']]
        ]
        words, mask = new_gen(ds, fd['nn'])

        return render_template('data2.html', form_data=fd, words=words, xlen=len(words), mask=mask)

@app.route('/data3', methods=['POST', 'GET'])
def data3():
    if request.method == 'GET':
        return "The URL /data3 is accessed directly. Try going to '/new3' to submit form"
    if request.method == 'POST':
        fd = request.form
        ds = [
            [fd['r1g1'], fd['r1g2'], fd['r1g3'], fd['r1g4'], fd['r1g5']],
            [fd['r2y1'], fd['r2y2'], fd['r2y3'], fd['r2y4'], fd['r2y5']],
            [fd['r3y1'], fd['r3y2'], fd['r3y3'], fd['r3y4'], fd['r3y5']],
            [fd['r4y1'], fd['r4y2'], fd['r4y3'], fd['r4y4'], fd['r4y5']],
            [fd['r5y1'], fd['r5y2'], fd['r5y3'], fd['r5y4'], fd['r5y5']],
            [fd['r6y1'], fd['r6y2'], fd['r6y3'], fd['r6y4'], fd['r6y5']],
        ]
        words, mask = new3_gen(ds, fd['nn'])
        return render_template('data2.html', form_data=fd, words=words, xlen=len(words), mask=mask)


@app.route('/TT1/')
def send_tt1():
    return send_from_directory(app.static_folder, 'Timetable 10 Cambridge to Ely, Peterborough and Norwich Large Print.pdf')
@app.route('/TT2/')
def send_tt2():
    return send_from_directory(app.static_folder, 'Timetable 12 Cambridge and Stansted Airport to London Large Print.pdf')
@app.route('/TT3/')
def send_tt3():
    return send_from_directory(app.static_folder, "Timetable 13 King's Lynn and Ely to London (direct services) Large Print.pdf")

if __name__ == "__main__":
    app.run()
