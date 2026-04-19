// --- Solver state ---
let allWords = [];
let candidates = [];
let notInWord = new Set();
let inWord = new Set();
let knownLetters = ['', '', '', '', ''];
let knownWrongPlacements = [[], [], [], [], []];
let multiLetters = {};

let currentWord = '';
let tileStates = ['X', 'X', 'X', 'X', 'X'];
let guessHistory = [];
let solved = false;

// --- Solver logic ---

function filterWords(words, known, wrongPlacements, inW, notInW, multiL) {
  for (let j = 0; j < 5; j++) {
    if (known[j] !== '') {
      words = words.filter(w => w[j] === known[j]);
    }
  }
  for (const letter of inW) {
    words = words.filter(w => w.includes(letter));
  }
  for (const letter of notInW) {
    words = words.filter(w => !w.includes(letter));
  }
  for (let j = 0; j < 5; j++) {
    for (const letter of wrongPlacements[j]) {
      words = words.filter(w => w[j] !== letter);
    }
  }
  for (const [letter, count] of Object.entries(multiL)) {
    words = words.filter(w => w.split('').filter(c => c === letter).length >= count);
  }
  return words;
}

function calculateLetterFrequency(words, known) {
  const freq = {};
  for (const word of words) {
    for (let i = 0; i < word.length; i++) {
      if (known[i] !== '') continue;
      const l = word[i];
      freq[l] = (freq[l] || 0) + 1;
    }
  }
  return freq;
}

function getTopSuggestions(words, known, n = 15) {
  if (words.length <= n) return words.map(w => w);
  const freq = calculateLetterFrequency(words, known);
  const scored = words.map(word => {
    const seen = new Set();
    let score = 0;
    for (let i = 0; i < word.length; i++) {
      const l = word[i];
      if (known[i] !== '' || seen.has(l)) continue;
      seen.add(l);
      score += freq[l] || 0;
    }
    return { word, score };
  });
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, n).map(s => s.word);
}

function processGuess(guess, result) {
  const guessLetterFreq = {};
  const yellowLetters = new Set();
  const potentiallyNotInWord = [];

  for (let j = 0; j < 5; j++) {
    const letter = guess[j];
    if (result[j] === 'X') {
      potentiallyNotInWord.push(letter);
    } else {
      inWord.add(letter);
      guessLetterFreq[letter] = (guessLetterFreq[letter] || 0) + 1;
      if (result[j] === 'I') {
        knownWrongPlacements[j].push(letter);
        yellowLetters.add(letter);
      } else if (result[j] === 'O') {
        knownLetters[j] = letter;
      }
    }
  }

  for (const [letter, count] of Object.entries(guessLetterFreq)) {
    if (count >= 2 && yellowLetters.has(letter)) {
      multiLetters[letter] = Math.max(multiLetters[letter] || 0, count);
    }
  }

  for (const letter of potentiallyNotInWord) {
    if (!inWord.has(letter)) {
      notInWord.add(letter);
    }
  }

  candidates = filterWords(candidates, knownLetters, knownWrongPlacements, inWord, notInWord, multiLetters);
}

function resetState() {
  candidates = [...allWords];
  notInWord = new Set();
  inWord = new Set();
  knownLetters = ['', '', '', '', ''];
  knownWrongPlacements = [[], [], [], [], []];
  multiLetters = {};
  currentWord = '';
  tileStates = ['X', 'X', 'X', 'X', 'X'];
  guessHistory = [];
  solved = false;
}

// --- UI ---

function cycleTile(index) {
  if (!currentWord || currentWord.length < 5 || solved) return;
  const states = ['X', 'I', 'O'];
  const current = tileStates[index];
  tileStates[index] = states[(states.indexOf(current) + 1) % 3];
  renderActiveTiles();
}

function renderActiveTiles() {
  for (let i = 0; i < 5; i++) {
    const tile = document.getElementById(`tile-${i}`);
    const letter = currentWord[i] || '';
    tile.textContent = letter.toUpperCase();
    if (letter) {
      tile.dataset.state = tileStates[i];
      tile.classList.remove('empty');
    } else {
      tile.dataset.state = 'X';
      tile.classList.add('empty');
    }
  }
}

function renderHistory() {
  const el = document.getElementById('history');
  if (guessHistory.length === 0) {
    el.innerHTML = '';
    return;
  }
  let html = '<div class="history-label">Past Guesses</div>';
  for (const { word, result } of guessHistory) {
    html += '<div class="history-row">';
    for (let i = 0; i < 5; i++) {
      html += `<div class="history-tile ${result[i]}">${word[i].toUpperCase()}</div>`;
    }
    html += '</div>';
  }
  el.innerHTML = html;
}

function renderResults() {
  const el = document.getElementById('results');
  const countEl = document.getElementById('remaining-count');
  const suggestEl = document.getElementById('suggestions');

  el.classList.remove('hidden');

  if (solved) {
    el.innerHTML = `<div class="solved-banner">You solved it! 🎉</div>`;
    return;
  }

  if (candidates.length === 0) {
    el.innerHTML = `<div class="remaining-count"><strong>No words remaining</strong> — check your inputs and try resetting.</div>`;
    return;
  }

  const suggestions = getTopSuggestions(candidates, knownLetters);
  const chips = suggestions.map(w => `<div class="suggestion-chip">${w.toUpperCase()}</div>`).join('');

  el.innerHTML = `
    <div class="remaining-count">
      <strong>${candidates.length}</strong> word${candidates.length === 1 ? '' : 's'} remaining
    </div>
    <div class="suggestions-label">Top suggestions</div>
    <div class="suggestions-grid">${chips}</div>
  `;
}

function setStatus(msg) {
  document.getElementById('status').textContent = msg;
}

function onGuessInput(e) {
  const raw = e.target.value.replace(/[^a-zA-Z]/g, '').toLowerCase().slice(0, 5);
  e.target.value = raw.toUpperCase();
  currentWord = raw;
  tileStates = ['X', 'X', 'X', 'X', 'X'];
  renderActiveTiles();
  setStatus('');
  document.getElementById('submitBtn').disabled = (raw.length !== 5 || solved);
}

function submitGuess() {
  if (!currentWord || currentWord.length !== 5) return;

  const guess = currentWord;
  const result = [...tileStates];

  const isSolved = result.every(s => s === 'O');

  processGuess(guess, result);
  guessHistory.push({ word: guess, result });

  if (isSolved) solved = true;

  renderHistory();
  renderResults();

  // Reset input for next guess
  document.getElementById('guessInput').value = '';
  currentWord = '';
  tileStates = ['X', 'X', 'X', 'X', 'X'];
  renderActiveTiles();
  document.getElementById('submitBtn').disabled = true;
  setStatus('');

  if (!isSolved) {
    document.getElementById('guessInput').focus();
  }
}

function resetGame() {
  resetState();
  document.getElementById('guessInput').value = '';
  renderActiveTiles();
  renderHistory();
  document.getElementById('results').classList.add('hidden');
  document.getElementById('submitBtn').disabled = true;
  setStatus('');

  // Show initial suggestions
  renderResults();
  document.getElementById('guessInput').focus();
}

// --- Init ---

async function init() {
  try {
    const response = await fetch('all_words.txt');
    if (!response.ok) throw new Error('Failed to load word list');
    const text = await response.text();
    allWords = text.split('\n').map(w => w.trim().toLowerCase()).filter(w => w.length === 5);
    candidates = [...allWords];

    document.getElementById('guessInput').addEventListener('input', onGuessInput);

    // Show initial suggestions
    renderResults();
    document.getElementById('guessInput').focus();
  } catch (err) {
    setStatus('Failed to load word list. Please refresh.');
    console.error(err);
  }
}

document.addEventListener('DOMContentLoaded', init);
