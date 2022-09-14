"""
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

"""

def isvalidguess(guess):
  if len(guess) != 5:
    return False
  return True

def isvalidresult(result):
  if len(result) != 5:
    return False
  for letter in result:
    if letter != 'X' and letter != 'I' and letter != 'O':
      return False
  return True

def help():
  print("Welcome to Wordle Solver! What step do you need help with?")
  print("For results, X denotes not in word, I denotes in word but wrong place, and O denotes letter in correct spot.")

def main():
  # Using readlines()
  all_words_file = open('all_words.txt', 'r')
  words = all_words_file.readlines()
  all_words_file.close

  # Strips the newline character
  for word in words:
    word = word.strip()

  # Step 2: get web URL from input
  print("Welcome to Wordle Solver! First, please input your first guess")
  guess = input("Guess a five letter word: ")
  while not isvalidguess(guess):
    if guess == "help":
      help()
    guess = input("Please guess a word with five letters: ")

  print("Thanks. Now submit the results from the game.")
  guess_result = input("Results (example 'XXIXO'): ")
  while not isvalidresult(guess_result):
    if guess_result == "help":
      help()
    guess_result = input("Results should only be made up of X/I/O and be 5 characters long: ")

  # Time to start filtering and stuff
  notinword = set()
  inword = set()
  knownletters = ['' for i in range(5)]
  knownwrongplacements = [[] for i in range(5)]

  while guess_result != "OOOOO":
    potentiallynotinword = []
    for i in range(5):
      if guess_result[i] == "O":
        inword.add(guess[i])
        knownletters[i] = guess[i]
      elif guess_result[i] == "I":
        inword.add(guess[i])
        knownwrongplacements[i].append(guess[i])
      elif guess_result[i] == "X":
        potentiallynotinword.append(guess[i])
    
    for letter in potentiallynotinword:
      if letter not in inword:
        notinword.add(letter)

    # FILTER ON MAIN LIST
    prevvalidwordscount = len(words)

    print("not in word: " + str(notinword))
    print("in word: " + str(inword))
    print("known letters: " + str(knownletters))
    print("known wrong placements: " + str(knownwrongplacements))

    # filter first on correct letter position words
    for i in range(len(knownletters)):
      if knownletters[i] != '':
        words = [word for word in words if word[i] == knownletters[i]]

    # then filter on having correct letters
    for letter in inword:
      words = [word for word in words if letter in word]

    # then filter on not having incorrect letters
    for letter in notinword:
      words = [word for word in words if letter not in word]

    # then filter on not having right letters in wrong placements
    for i in range(len(knownwrongplacements)):
      if knownwrongplacements[i]:
        for wrongplacement in knownwrongplacements[i]:
          words = [word for word in words if word[i] != wrongplacement]
    
    newvalidwordscount = len(words)
    print("Number of possible words reduced from " + str(prevvalidwordscount) + " down to " + str(newvalidwordscount) + ".")

    someremainingwords = []
    for i in range(min(newvalidwordscount, 12)):
      someremainingwords.append(words[i].strip())
    print("Some of the valid words remaining: " + str(someremainingwords))

    guess = input("Guess another word: ")
    while not isvalidguess(guess):
      if guess == "help":
        help()
      guess = input("Please guess a word with five letters: ")

    print("Thanks. Now submit the results from the game.")
    guess_result = input("Results (example 'XXIXO'): ")
    while not isvalidresult(guess_result):
      if guess_result == "help":
        help()
      guess_result = input("Results should only be made up of X/I/O and be 5 characters long: ")
  
  print("Congrats! The word is " + guess)


if __name__ == '__main__':
  # CODE STARTS HERE AND EXECUTES main()
  main()
