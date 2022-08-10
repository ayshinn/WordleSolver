## Curse Word Calculator

### HOW TO USE ###
On the command line, you'd run
`python3 CurseWordCalculator.py`
and it'll prompt you:
`What is the author? (Only first letter capitalized):`
and
`What is the song name? (all lower case, replace spaces with '-'):`.

It'll generate a URL for genius.com, grab lyrics, and then parse through them for any matches to bad words.

(I personally haven't used jupyter but it should run in there I think?
You may need to figure how to do that, copy this code in a notebook or something)


curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
ls
python3 get-pip.py
python3 -m pip install --upgrade pip
pip3 install BeautifulSoup4
python3 CurseWordCalculator.py
pip3 install requests
python3 CurseWordCalculator.py

