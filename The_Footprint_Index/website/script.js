function calculate() {
  const input = document.getElementById("input").value;
  const result = parseInt(input) * 100;
  document.getElementById("result").textContent = `Result: ${result}`;
}