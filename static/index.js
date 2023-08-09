const header = document.querySelector("#header");
const form = document.getElementById("api-form");
const input = document.getElementById("apiExample");
const btn = document.querySelector("#form-btn");
const dataDisplay = document.getElementById("display-data");
const pokemonLink = document.querySelector("#pokemon-link");
const typesLink = document.querySelector("#types-link");
const combatLink = document.querySelector("#combat-link");
const descriptionsLink = document.querySelector("#descriptions-link");
const imagesLink = document.querySelector("#images-link");

async function handleSubmit(e) {
  e.preventDefault();
  createAccordion();

  //   accordionMainDiv.appendChild(createAccordionItem())
  //   dataDisplay.innerHTML = JSON.stringify(jsonData, null, 4);
}

function createAccordionItem(btnText, bodyInfo) {
  const accordionItemDiv = document.createElement("div");
  const accHeader = document.createElement("h2");
  const accBtn = document.createElement("button");
  const hiddenDiv = document.createElement("div");
  let textDiv;
  let name = "";
  if (typeof bodyInfo === "object" && bodyInfo !== null) {
    textDiv = document.createElement("pre");
    name = bodyInfo["name"] || "";
    bodyInfo = JSON.stringify(bodyInfo, null, 4);
  } else {
    textDiv = document.createElement("div");
  }

  // Main creation
  textDiv.className = "accordion-body";
  textDiv.innerHTML = bodyInfo;
  hiddenDiv.className = "accordion-collapse collapse";
  hiddenDiv.id = btnText;
  hiddenDiv.setAttribute("data-bs-parent", "#accordionExample");
  accBtn.className = "accordion-button";
  accBtn.type = "button";
  accBtn.setAttribute("data-bs-toggle", "collapse");
  accBtn.setAttribute("data-bs-target", "#" + btnText);
  accBtn.setAttribute("aria-expanded", false);
  accBtn.setAttribute("aria-controls", btnText);
  accBtn.innerText = btnText + "   " + name;
  accHeader.className = "accordion-header";
  accordionItemDiv.className = "accordion-item";

  // Logical building
  accHeader.appendChild(accBtn);
  hiddenDiv.appendChild(textDiv);
  accordionItemDiv.appendChild(accHeader);
  accordionItemDiv.appendChild(hiddenDiv);
  return accordionItemDiv;
}

async function createAccordion() {
  dataDisplay.innerHTML = "";
  const response = await fetch(input.value);
  const jsonData = await response.json();
  keys = Object.keys(jsonData);
  const accordionMainDiv = document.createElement("div");
  accordionMainDiv.className = "accordion";
  accordionMainDiv.id = "accordionExample";
  for (key in keys) {
    if (typeof jsonData[keys[key]] !== "undefined") {
      const itemDiv = createAccordionItem(keys[key], jsonData[keys[key]]);
      accordionMainDiv.appendChild(itemDiv);
    }
  }
  dataDisplay.appendChild(accordionMainDiv);
}
// Drop down links logic

function handleLink(e) {
  e.preventDefault();
  if (this.id.includes("pokemon")) {
    input.value = "http://127.0.0.1:5000/api/pokemons";
    btn.click();
  } else if (this.id.includes("types")) {
    input.value = "http://127.0.0.1:5000/api/types";
    btn.click();
  } else if (this.id.includes("combat")) {
    input.value = "http://127.0.0.1:5000/api/types-combat";
    btn.click();
  } else if (this.id.includes("descriptions")) {
    input.value = "http://127.0.0.1:5000/api/description";
    btn.click();
  } else {
    input.value = "http://127.0.0.1:5000/api/image-paths";
    btn.click();
  }
}

pokemonLink.addEventListener("click", handleLink);
typesLink.addEventListener("click", handleLink);
combatLink.addEventListener("click", handleLink);
descriptionsLink.addEventListener("click", handleLink);
imagesLink.addEventListener("click", handleLink);
form.addEventListener("submit", handleSubmit);
