/* ================================
   CANVAS SETUP
================================ */

const canvas = document.getElementById("cityCanvas");
const ctx = canvas.getContext("2d");

const gridSize = 30;
const tileSize = 32;

canvas.width = gridSize * tileSize;
canvas.height = gridSize * tileSize;


/* ================================
   GLOBAL STATE (FROM BACKEND)
================================ */

let agents = [];
let foodPrice = 0;


/* ================================
   TILE TYPES
================================ */

const TILE = {
    GRASS: 0,
    ROAD: 1,
    HOUSE: 2,
    WORK: 3,
    MARKET: 4
};


/* ================================
   SPRITES
================================ */

const sprites = {
    grass: new Image(),
    road: new Image(),
    house: new Image(),
    office: new Image(),
    market: new Image()
};

sprites.grass.src = "sprites/grass.png";
sprites.road.src = "sprites/road.png";
sprites.house.src = "sprites/house.png";
sprites.office.src = "sprites/office.png";
sprites.market.src = "sprites/market.png";


/* ================================
   MAP INITIALIZATION
================================ */

const map = [];

for (let y = 0; y < gridSize; y++) {
    const row = [];
    for (let x = 0; x < gridSize; x++) {
        row.push(TILE.GRASS);
    }
    map.push(row);
}


/* ================================
   ROAD GRID
================================ */

for (let i = 0; i < gridSize; i++) {
    map[10][i] = TILE.ROAD;
    map[20][i] = TILE.ROAD;
    map[i][10] = TILE.ROAD;
    map[i][20] = TILE.ROAD;
}


/* ================================
   BUILDINGS
================================ */

function placeBuilding(x, y, type) {
    map[y][x] = type;
    map[y][x + 1] = type;
    map[y + 1][x] = type;
    map[y + 1][x + 1] = type;
}

// Residential (top-left)
for (let y = 2; y < 8; y += 3)
    for (let x = 2; x < 8; x += 3)
        placeBuilding(x, y, TILE.HOUSE);

// Work
for (let y = 12; y < 18; y += 3)
    for (let x = 3; x < 9; x += 3)
        placeBuilding(x, y, TILE.WORK);

// Market
for (let y = 12; y < 18; y += 3)
    for (let x = 22; x < 27; x += 3)
        placeBuilding(x, y, TILE.MARKET);

// Residential (bottom)
for (let y = 22; y < 28; y += 3)
    for (let x = 12; x < 18; x += 3)
        placeBuilding(x, y, TILE.HOUSE);


/* ================================
   BACKEND CONNECTION
================================ */

async function fetchSimulation() {
    try {
        const res = await fetch("http://127.0.0.1:5000/step");
        const data = await res.json();
        console.log("DATA FROM BACKEND:", data);  
        agents = data.agents;
        foodPrice = data.price;

    } catch (err) {
        console.error("Fetch error:", err);
    }
}


/* ================================
   DRAW TILE
================================ */

function drawTile(x, y, type) {
    const px = x * tileSize;
    const py = y * tileSize;

    if (type === TILE.GRASS)
        ctx.drawImage(sprites.grass, px, py, tileSize, tileSize);

    else if (type === TILE.ROAD)
        ctx.drawImage(sprites.road, px, py, tileSize, tileSize);

    else if (type === TILE.HOUSE)
        ctx.drawImage(sprites.house, px, py, tileSize, tileSize);

    else if (type === TILE.WORK)
        ctx.drawImage(sprites.office, px, py, tileSize, tileSize);

    else if (type === TILE.MARKET)
        ctx.drawImage(sprites.market, px, py, tileSize, tileSize);
}


/* ================================
   DRAW MAP
================================ */

function drawMap() {
    for (let y = 0; y < gridSize; y++) {
        for (let x = 0; x < gridSize; x++) {
            drawTile(x, y, map[y][x]);
        }
    }
}


/* ================================
   DRAW AGENTS (REAL DATA)
================================ */

function drawAgents() {
    agents.forEach(agent => {

        let color;

        if (agent.action === "work") {
            color = "#4CAF50"; // green → working
        } 
        else if (agent.action === "buy_food") {
            color = "#2196F3"; // blue → buying food
        } 
        else {
            color = "#9E9E9E"; // gray → exploring
        }

        const ax = agent.x * tileSize + tileSize / 2;
        const ay = agent.y * tileSize + tileSize / 2;

        ctx.beginPath();
        ctx.fillStyle = color;
        ctx.arc(ax, ay, 6, 0, Math.PI * 2);
        ctx.fill();
    });
}

/* ================================
   HUD (PRICE DISPLAY)
================================ */

function drawHUD() {
    ctx.fillStyle = "white";
    ctx.font = "14px monospace";
    ctx.fillText(`Food Price: ${foodPrice}`, 10, 20);
}


/* ================================
   RENDER
================================ */

function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawMap();
    drawAgents();
    drawHUD();
}


/* ================================
   GAME LOOP
================================ */

async function gameLoop() {
    await fetchSimulation();
    render();
}


/* ================================
   START (SPRITE SAFE LOAD)
================================ */

window.onload = async () => {

    // wait until all sprites load
    const allLoaded = Object.values(sprites).every(img => img.complete);

    if (!allLoaded) {
        setTimeout(window.onload, 100);
        return;
    }

    await fetchSimulation();
    render();

    setInterval(() => {
        gameLoop();
    }, 400);
};