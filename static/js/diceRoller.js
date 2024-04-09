function rollDice() {
  const dice = document.getElementById("diceSelect").value;
  const result = Math.floor(Math.random() * dice) + 1;
  document.getElementById("result").innerText = "You rolled: " + result;
}
