const canvas = document.getElementById("cityCanvas");
const ctx = canvas.getContext("2d");

const gridSize = 30;
const tileSize = 32;

/* ---------- TILE TYPES ---------- */

const TILE = {
    GRASS: 0,
    ROAD: 1,
    HOUSE: 2,
    WORK: 3,
    MARKET: 4
};

/* ---------- SPRITES ---------- */

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

/* ---------- MAP ---------- */

const map = [];

for (let y = 0; y < gridSize; y++) {

    const row = [];

    for (let x = 0; x < gridSize; x++) {
        row.push(TILE.GRASS);
    }

    map.push(row);
}

/* ---------- ROAD GRID ---------- */

for (let i = 0; i < gridSize; i++) {

    map[10][i] = TILE.ROAD;
    map[20][i] = TILE.ROAD;

    map[i][10] = TILE.ROAD;
    map[i][20] = TILE.ROAD;
}

/* ---------- BUILDING FUNCTION ---------- */

function placeBuilding(x, y, type) {

    map[y][x] = type;
    map[y][x + 1] = type;
    map[y + 1][x] = type;
    map[y + 1][x + 1] = type;
}

/* ---------- RESIDENTIAL DISTRICT (TOP LEFT) ---------- */

for (let y = 2; y < 8; y += 3) {
    for (let x = 2; x < 8; x += 3) {

        placeBuilding(x, y, TILE.HOUSE);

    }
}

/* ---------- WORK DISTRICT (CENTER LEFT) ---------- */

for (let y = 12; y < 18; y += 3) {
    for (let x = 3; x < 9; x += 3) {

        placeBuilding(x, y, TILE.WORK);

    }
}

/* ---------- MARKET DISTRICT (RIGHT SIDE) ---------- */

for (let y = 12; y < 18; y += 3) {
    for (let x = 22; x < 27; x += 3) {

        placeBuilding(x, y, TILE.MARKET);

    }
}

/* ---------- RESIDENTIAL DISTRICT (BOTTOM) ---------- */

for (let y = 22; y < 28; y += 3) {
    for (let x = 12; x < 18; x += 3) {

        placeBuilding(x, y, TILE.HOUSE);

    }
}

/* ---------- AGENTS ---------- */

const agents = [];

for (let i = 0; i < 40; i++) {

    agents.push({
        x: Math.floor(Math.random() * gridSize),
        y: Math.floor(Math.random() * gridSize)
    });
}

/* ---------- DRAW TILE ---------- */

function drawTile(x, y, type) {

    const px = x * tileSize;
    const py = y * tileSize;

    if (type === TILE.GRASS)
        ctx.drawImage(sprites.grass, px, py, tileSize, tileSize);

    if (type === TILE.ROAD)
        ctx.drawImage(sprites.road, px, py, tileSize, tileSize);

    if (type === TILE.HOUSE)
        ctx.drawImage(sprites.house, px, py, tileSize, tileSize);

    if (type === TILE.WORK)
        ctx.drawImage(sprites.office, px, py, tileSize, tileSize);

    if (type === TILE.MARKET)
        ctx.drawImage(sprites.market, px, py, tileSize, tileSize);
}

/* ---------- DRAW MAP ---------- */

function drawMap() {

    for (let y = 0; y < gridSize; y++) {

        for (let x = 0; x < gridSize; x++) {

            drawTile(x, y, map[y][x]);

        }
    }
}

/* ---------- DRAW AGENTS ---------- */

function drawAgents() {

    agents.forEach(agent => {

        ctx.beginPath();

        ctx.fillStyle = "yellow";

        ctx.arc(
            agent.x * tileSize + tileSize / 2,
            agent.y * tileSize + tileSize / 2,
            5,
            0,
            Math.PI * 2
        );

        ctx.fill();
    });
}

/* ---------- MOVE AGENTS ---------- */

function moveAgents(){

    agents.forEach(agent=>{

        const directions = [
            {dx:1,dy:0},
            {dx:-1,dy:0},
            {dx:0,dy:1},
            {dx:0,dy:-1}
        ]

        const dir = directions[Math.floor(Math.random()*4)]

        const nx = agent.x + dir.dx
        const ny = agent.y + dir.dy

        if(nx>=0 && nx<gridSize && ny>=0 && ny<gridSize){

            if(map[ny][nx] === TILE.ROAD){
                agent.x = nx
                agent.y = ny
            }

        }

    })

}

/* ---------- RENDER ---------- */

function render() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawMap();
    drawAgents();
}

/* ---------- GAME LOOP ---------- */

function gameLoop() {

    moveAgents();
    render();
}

window.onload = () => {

    render();
    setInterval(gameLoop, 400);
};