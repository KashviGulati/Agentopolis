/* ================================
   CANVAS SETUP
================================ */

const canvas = document.getElementById("cityCanvas");
const ctx = canvas.getContext("2d");

const gridSize = 30;

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

resizeCanvas();
window.addEventListener("resize", resizeCanvas);


/* ================================
   GLOBAL STATE
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
   MAP
================================ */

const map = [];

for (let y = 0; y < gridSize; y++) {
    const row = [];
    for (let x = 0; x < gridSize; x++) row.push(TILE.GRASS);
    map.push(row);
}

for (let i = 0; i < gridSize; i++) {
    map[10][i] = TILE.ROAD;
    map[20][i] = TILE.ROAD;
    map[i][10] = TILE.ROAD;
    map[i][20] = TILE.ROAD;
}

function placeBuilding(x, y, type) {
    map[y][x] = type;
    map[y][x + 1] = type;
    map[y + 1][x] = type;
    map[y + 1][x + 1] = type;
}

// districts
for (let y = 2; y < 8; y += 3)
    for (let x = 2; x < 8; x += 3)
        placeBuilding(x, y, TILE.HOUSE);

for (let y = 12; y < 18; y += 3)
    for (let x = 3; x < 9; x += 3)
        placeBuilding(x, y, TILE.WORK);

for (let y = 12; y < 18; y += 3)
    for (let x = 22; x < 27; x += 3)
        placeBuilding(x, y, TILE.MARKET);

for (let y = 22; y < 28; y += 3)
    for (let x = 12; x < 18; x += 3)
        placeBuilding(x, y, TILE.HOUSE);


/* ================================
   FETCH BACKEND
================================ */

async function fetchSimulation() {
    try {
        const res = await fetch("http://127.0.0.1:5000/step");
        const data = await res.json();

        agents = data.agents;
        foodPrice = data.price;

    } catch (err) {
        console.error("Fetch error:", err);
    }
}


/* ================================
   DRAW MAP (FULLSCREEN)
================================ */

function drawMap(tileSizeX, tileSizeY) {

    for (let y = 0; y < gridSize; y++) {
        for (let x = 0; x < gridSize; x++) {

            const px = x * tileSizeX;
            const py = y * tileSizeY;

            const type = map[y][x];

            if (type === TILE.GRASS)
                ctx.drawImage(sprites.grass, px, py, tileSizeX, tileSizeY);

            else if (type === TILE.ROAD)
                ctx.drawImage(sprites.road, px, py, tileSizeX, tileSizeY);

            else if (type === TILE.HOUSE)
                ctx.drawImage(sprites.house, px, py, tileSizeX, tileSizeY);

            else if (type === TILE.WORK)
                ctx.drawImage(sprites.office, px, py, tileSizeX, tileSizeY);

            else if (type === TILE.MARKET)
                ctx.drawImage(sprites.market, px, py, tileSizeX, tileSizeY);
        }
    }
}


/* ================================
   DRAW AGENTS
================================ */

function drawAgents(tileSizeX, tileSizeY) {

    agents.forEach(agent => {

        let color;

        if (agent.action === "work") color = "#4CAF50";
        else if (agent.action === "buy_food") color = "#2196F3";
        else color = "#9E9E9E";

        const ax = agent.x * tileSizeX + tileSizeX / 2;
        const ay = agent.y * tileSizeY + tileSizeY / 2;

        ctx.beginPath();
        ctx.fillStyle = color;
        ctx.arc(ax, ay, Math.min(tileSizeX, tileSizeY) * 0.3, 0, Math.PI * 2);
        ctx.fill();
    });
}


/* ================================
   HUD
================================ */

function drawHUD() {

    ctx.fillStyle = "rgba(0,0,0,0.6)";
    ctx.fillRect(10, 10, 200, 70);

    ctx.fillStyle = "#00e5ff";
    ctx.font = "14px monospace";

    ctx.fillText(`Agents: ${agents.length}`, 20, 30);
    ctx.fillText(`Food Price: ${foodPrice}`, 20, 50);
}


/* ================================
   RENDER
================================ */

function render() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const tileSizeX = canvas.width / gridSize;
    const tileSizeY = canvas.height / gridSize;

    drawMap(tileSizeX, tileSizeY);
    drawAgents(tileSizeX, tileSizeY);
    drawHUD();
}


/* ================================
   LOOP
================================ */

async function gameLoop() {
    await fetchSimulation();
    render();
}


/* ================================
   START
================================ */

window.onload = async () => {

    await fetchSimulation();
    render();

    setInterval(gameLoop, 400);
};