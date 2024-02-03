// Replace with your backend API endpoint URL
const apiUrl = "https://your-backend-api.com/calculate-emissions";

// Fetch company list from your database using appropriate method (e.g., XMLHttpRequest, fetch)
// Populate the company select element with retrieved data

// Example company data (replace with your actual data)
const companies = [
  { code: "CRDA", name: "Croda International" },
  { code: "DGE", name: "Diageo plc" },
  { code: "BRBY", name: "Burberry Group plc" },
];

companies.forEach((company) => {
  const option = document.createElement("option");
  option.value = company.code;
  option.textContent = company.name;
  document.getElementById("company-select").appendChild(option);
});

function calculateEmissionRatio() {
  const selectedCompany = document.getElementById("company-select").value;
  const selectedTransport = document.getElementById("transport-select").value;

  fetch(`${apiUrl}?company=${selectedCompany}&transport=${selectedTransport}`)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("result").textContent = `Emission Ratio: ${data.ratio}`;
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
      document.getElementById("result").textContent =
        "An error occurred. Please try again later.";
    });
}
