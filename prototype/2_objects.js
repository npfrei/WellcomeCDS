const width = 960;
const height = 600;
  
const imageSize = 100;

const svg = d3.select("#chart")
  .attr("viewBox", [0, 0, width, height]);

let link, node;
let nodesData = [], linksData = [];
let centralNode, sideNodes;

Promise.all([
  d3.json("aidssaint.json")
]).then(([data]) => {
  const root = d3.hierarchy(data);
  linksData = root.links();
  nodesData = root.descendants();

  
  // Find central node (centrality = 1) and side nodes (centrality = 0)
  const centralNode = nodesData.find(d => d.data.centrality === 1);
  const sideNodes = nodesData.filter(d => d.data.centrality === 0);

  // Place the central node in the middle horizontally with slight noise
  if (centralNode) {
    centralNode.x = width / 2 + (Math.random() - 0.5) * 100;
    centralNode.y = height / 2 + (Math.random() - 0.5) * 100;
  }

  // Place the side nodes to the left and right
  if (sideNodes.length >= 2) {
    sideNodes[0].x = width / 2 - 250 + (Math.random() - 0.5) * 100;
    sideNodes[0].y = height / 2 + (Math.random() - 0.5) * 100;

    sideNodes[1].x = width / 2 + 250 + (Math.random() - 0.5) * 100;
    sideNodes[1].y = height / 2 + (Math.random() - 0.5) * 100;
  }
  
  
  const simulation = d3.forceSimulation(nodesData)
    .force("link", d3.forceLink(linksData).distance(150).strength(1).id(d => d.data.id))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2))
//    .force("y", d3.forceY(height / 2).strength(0.05))
//    .force("x", d3.forceX(width / 2).strength(0.005))

    .stop(); 

//  function customRepulsion(strength = 30) {
//
//    return () => {
//      for (let i = 0; i < nodesData.length; ++i) {
//        const a = nodesData[i];
//        for (let j = i + 1; j < nodesData.length; ++j) {
//          const b = nodesData[j];
//          const dx = b.x - a.x;
//          const dy = b.y - a.y;
//          const distSq = dx * dx + dy * dy + 0.01; // Avoid division by zero
//          const force = strength / distSq;
//  
//          const fx = force * dx;
//          const fy = force * dy;
//
//          a.vx -= fx;
//          a.vy -= fy;
//          b.vx += fx;
//          b.vy += fy;
//        }
//      }
//    };
//  }

//  simulation.force("customRepulsion", customRepulsion(10));

  
  
  for (let i = 0; i < 300; ++i) simulation.tick(); // precompute layout

  link = svg.append("g")
    .attr("stroke", "#fff")
    .attr("stroke-opacity", 0.7)
    .attr("stroke-width", 4)
    .selectAll("line")
    .data(linksData)
    .join("line");
  
  

//  node = svg.append("g")
//      .attr("stroke", "#000")
//      .attr("stroke-width", 1.5)
//    .selectAll("circle")
//    .data(nodesData)
//    .join("circle")
//      .attr("r", 5)
//      .attr("fill", d => d.children ? "#555" : "#999")
//      .call(drag(simulation));
  

  // Sort by ratio, then by depth
  nodesData.sort((a, b) => {
    if (a.data.ratio === b.data.ratio) {
      return b.depth - a.depth; 
    }
    return a.data.ratio - b.data.ratio;
  });


  
//  node = svg.append("g")
//  .selectAll("image")
//  .data(nodesData)
//  .join("image")
//    .attr("xlink:href", d => d.data.url) 
//    .attr("width", d => imageSize * d.data.ratio)
//    .attr("height", d => imageSize * d.data.ratio)
//    .attr("x", d => d.x - imageSize / 2)
//    .attr("y", d => d.y - imageSize / 2);

    node = svg.append("g")
      .selectAll("image")
      .data(nodesData)
      .join("image")
        .attr("xlink:href", d => d.data.url)
        .attr("width", d => imageSize * d.data.ratio)
        .attr("height", d => imageSize * d.data.ratio)
        .attr("x", d => d.x - imageSize / 2)
        .attr("y", d => d.y - imageSize / 2)
        .style("opacity", 0) // start hidden
        .each(function(d, i) {
          d3.select(this)
            .transition()
            .delay(d.data.order * 2000)
            .duration(3000)
            .style("opacity", 1);
        });

    // Append <title> as separate selection
    svg.selectAll("image")
      .data(nodesData)
      .append("title")
      .text(d => d.data.name);

  
  
//  node.append("title")
//    .text(d => d.data.name);


  // Start animation
  animateFloating();
});



function cw(obj_ind){
  return 1 - 2 * (obj_ind % 2)
}

function animateFloating() {
  const amplitude = 2.5;
  const frequency = 0.001;
  const clockwise = 1 - 2 * Math.floor(Math.random()) // modulo 2 de l'index

  d3.timer((elapsed) => {
//    link
//      .attr("x1", d => d.source.x + Math.sin(elapsed * frequency + d.index) * amplitude)
//      .attr("y1", d => d.source.y + Math.cos(elapsed * frequency + d.index) * amplitude)
//      .attr("x2", d => d.target.x + Math.sin(elapsed * frequency + d.index + 1) * amplitude)
//      .attr("y2", d => d.target.y + Math.cos(elapsed * frequency + d.index + 1) * amplitude);

    node
      .attr("x", d => d.x + Math.sin(elapsed * frequency * cw(d.index) + d.index) * amplitude - imageSize / 2)
      .attr("y", d => d.y + Math.cos(elapsed * frequency * cw(d.index) + d.index) * amplitude - imageSize / 2)

  });
}

// make them appear in order (add attribute order: is that structure the best?)
