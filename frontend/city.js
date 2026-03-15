const canvas = document.getElementById("cityCanvas");
const ctx = canvas.getContext("2d");

const gridSize = 30;
const tileSize = 20;

/* ---------- CITY BUILDINGS ---------- */

const work = [
    {x:5,y:5},
    {x:12,y:10},
    {x:20,y:8}
]

const market = [
    {x:10,y:20},
    {x:25,y:15}
]

const housing = [
    {x:3,y:25},
    {x:7,y:23},
    {x:15,y:25},
    {x:18,y:24}
]

/* ---------- AGENTS ---------- */

const agents = []

for(let i=0;i<10;i++){

    agents.push({
        x: Math.floor(Math.random()*gridSize),
        y: Math.floor(Math.random()*gridSize)
    })

}

/* ---------- DRAW GRID ---------- */

function drawGrid(){

    for(let x=0;x<gridSize;x++){
        for(let y=0;y<gridSize;y++){

            ctx.strokeStyle="#66bb6a"

            ctx.strokeRect(
                x*tileSize,
                y*tileSize,
                tileSize,
                tileSize
            )
        }
    }
}

/* ---------- DRAW BUILDINGS ---------- */

function drawBuildings(){

    work.forEach(p=>{
        ctx.fillStyle="gray"
        ctx.fillRect(p.x*tileSize,p.y*tileSize,tileSize,tileSize)
    })

    market.forEach(p=>{
        ctx.fillStyle="blue"
        ctx.fillRect(p.x*tileSize,p.y*tileSize,tileSize,tileSize)
    })

    housing.forEach(p=>{
        ctx.fillStyle="purple"
        ctx.fillRect(p.x*tileSize,p.y*tileSize,tileSize,tileSize)
    })
}

/* ---------- DRAW AGENTS ---------- */

function drawAgents(){

    ctx.font = "16px Arial"

    agents.forEach(agent=>{

        ctx.fillText(
            "👤",
            agent.x*tileSize + 2,
            agent.y*tileSize + 16
        )

    })
}

/* ---------- MOVE AGENTS ---------- */

function moveAgents(){

    agents.forEach(agent=>{

        const dx = Math.floor(Math.random()*3) - 1
        const dy = Math.floor(Math.random()*3) - 1

        agent.x = Math.max(0,Math.min(gridSize-1,agent.x + dx))
        agent.y = Math.max(0,Math.min(gridSize-1,agent.y + dy))

    })
}

/* ---------- RENDER ---------- */

function render(){

    ctx.clearRect(0,0,600,600)

    drawGrid()
    drawBuildings()
    drawAgents()

}

/* ---------- GAME LOOP ---------- */

function gameLoop(){

    moveAgents()
    render()

}

setInterval(gameLoop,400)