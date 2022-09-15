"""
### HOW TO USE ###
On the command line, you'd run
`python3 wordle_solver.py`
and it'll prompt you:
`Guess a five letter word:`
and
`Results:`.

For help, type "h" or "help" at any point.
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

def takeguess():
  guess = input("Guess a five letter word: ")
  while not isvalidguess(guess):
    if guess == "help" or guess == "h":
      help()
    guess = input("Please guess a word with five letters: ")

  return guess

def submitresults():
  guess_result = input("Results: ")
  while not isvalidresult(guess_result):
    if guess_result == "help" or guess_result == "h":
      help()
    guess_result = input("Results should only be made up of X/I/O and be 5 characters long: ")
  return guess_result

def showbestremainingwords(words, knownletters):
  if len(words) < 20:
    print("Some of the valid words remaining: " + str(words) + "\n")
    return

  # TODO optimize this function to take in known letter positions and only optimize for missing letter spots
  letterfrequencydict = {}
  for word in words:
    word = word.strip()
    for i in range(len(word)):
      if knownletters[i] != "":
        # we only care to optimize for letter frequencies on parts of the word that is yet to be solved.
        continue
      letter = word[i]
      if letter in letterfrequencydict:
        letterfrequencydict[letter] += 1
      else:
        letterfrequencydict[letter] = 1

  remainingwordswithscores = []
  for word in words:
    word = word.strip()
    alreadyusedletters = set()
    score = 0

    # Get the "score" of the word based on how frequently its letters are used in remaining valid words
    for i in range(len(word)):
      letter = word[i]
      if knownletters[i] != "" or letter in alreadyusedletters:
        # we only care to optimize for letter frequencies on parts of the word that is yet to be solved and is unique.
        continue
      else:
        alreadyusedletters.add(letter)
        score += letterfrequencydict[letter]

    # Fetch the 20 most valuable words to use to print to the user
    if len(remainingwordswithscores) < 20:
      remainingwordswithscores.append([word, score])
    else:
      remainingwordswithscores.sort(key = lambda x: x[1], reverse = True)
      if score > remainingwordswithscores[-1][1]:
        remainingwordswithscores.pop()
        remainingwordswithscores.append([word, score])

  print("Some of the valid words remaining: " + str(remainingwordswithscores) + "\n")
  return

def main():
  # Reads in the list of 5 letter words available to us.
  all_words_file = open('all_words.txt', 'r')
  words = all_words_file.readlines()
  all_words_file.close

  # Strips the newline character
  for word in words:
    word = word.strip()

  # Prompts the user for their guess and the corresponding result
  print("Welcome to Wordle Solver! First, please input your first guess")
  guess = takeguess()
  print("Thanks. Now submit the results from the game.")
  guess_result = submitresults()

  notinword = set()
  inword = set()
  knownletters = ['' for i in range(5)]
  knownwrongplacements = [[] for i in range(5)]

  while guess_result != "OOOOO":
    # Gather information based on results on letter placement, and if each letter is in the word or not
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

    prevvalidwordscount = len(words)

    # Filters down the list of words that can possibly remain to guess.
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

    showbestremainingwords(words, knownletters)

    guess = takeguess()
    guess_result = submitresults()
  
  print("Congrats! The word is " + guess)


if __name__ == '__main__':
  main()
