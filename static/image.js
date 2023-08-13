const DEV_DOMAIN = "http://127.0.0.1:5000/";
const DEPLOYED_DOMAIN = "https://pokeinfo-api.onrender.com/";

const randomBtn = document.querySelector(".random-btn");
const backBtn = document.querySelector(".svg-arrow-img");

const handleClick = (e) => {
  e.preventDefault();
  const newId = Math.floor(Math.random() * (1008 - 1) + 1);
  const newURL = `${DEV_DOMAIN}pokemon-images/${newId}/show`;
  window.location.replace(newURL);
};

randomBtn.addEventListener("click", handleClick);
backBtn.addEventListener("click", () => {
  window.location.replace(DEV_DOMAIN);
});
