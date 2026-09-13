let menu = [];
let customerName = "";
let currentOrder = [];

document.addEventListener("DOMContentLoaded", function () {
  loadMenu();
});

function showMessage(text) {
  document.getElementById("message").innerHTML =
    '<div class="message-box">' + text + '</div>';
}

function showSection(sectionId) {
  const sections = document.querySelectorAll(".section");

  sections.forEach(function (section) {
    section.classList.remove("active");
  });

  if (sectionId !== "home") {
    document.getElementById(sectionId).classList.add("active");
  }

  if (sectionId === "menuSection") {
    loadMenu();
  }
}

function startOrdering() {
  const nameInput = document.getElementById("customerName");
  customerName = nameInput.value.trim();

  if (customerName === "") {
    showMessage("Please enter your name.");
    return;
  }

  document.getElementById("customerDisplay").textContent =
    "Customer: " + customerName;

  showMessage("Welcome, " + customerName + "! You can now view the food menu.");
  showSection("menuSection");
}

async function loadMenu() {
  try {
    const response = await fetch("api.php?action=menu");
    menu = await response.json();

    displayMenu();
    fillFoodSelect();
  } catch (error) {
    showMessage("Menu could not be loaded. Please check the backend/database.");
  }
}

function displayMenu() {
  const menuDiv = document.getElementById("menu");

  if (menu.length === 0) {
    menuDiv.innerHTML = "<p>No food items are currently available.</p>";
    return;
  }

  menuDiv.innerHTML = menu.map(function (item) {
    return `
      <div class="food-item">
        <div>
          <h3>${item.name}</h3>
          <div class="category">${item.category}</div>
          <div>${item.description}</div>
          <div class="price">RM${Number(item.price).toFixed(2)}</div>
        </div>
        <button onclick="chooseFood(${item.id})">Select</button>
      </div>
    `;
  }).join("");
}

function fillFoodSelect() {
  const select = document.getElementById("foodSelect");

  select.innerHTML = menu.map(function (item) {
    return `<option value="${item.id}">${item.name} - RM${Number(item.price).toFixed(2)}</option>`;
  }).join("");
}

function chooseFood(id) {
  document.getElementById("foodSelect").value = id;
  showSection("interactionSection");
}

function addSelectedItem() {
  if (customerName === "") {
    showMessage("Please enter your name first.");
    return;
  }

  const foodId = Number(document.getElementById("foodSelect").value);
  const quantity = Number(document.getElementById("quantity").value);

  if (!foodId) {
    showMessage("Please select a food item.");
    return;
  }

  if (!Number.isInteger(quantity) || quantity < 1) {
    showMessage("Quantity must be at least 1.");
    return;
  }

  const food = menu.find(function (item) {
    return Number(item.id) === foodId;
  });

  currentOrder.push({
    food_id: foodId,
    food_name: food.name,
    quantity: quantity
  });

  showMessage(
    quantity + " x " + food.name + " added to the current order."
  );

  document.getElementById("quantity").value = 1;
}