const width = 960;
const height = 600;
  
const imageSize = 100;

const svg = d3.select("#chart")
  .attr("viewBox", [0, 0, width, height]);

let link, node;
let nodesData = [], linksData = [];
let centralNode, sideNodes;
let animationStarted = false;

Promise.all([
  d3.json("aids.json")
]).then(([data]) => {
  const root = d3.hierarchy(data);
  linksData = root.links();
  nodesData = root.descendants();

  // Find central node (centrality = 1) and side nodes (centrality = 0)
  const centralNode = nodesData.find(d => d.data.centrality === 1);
  const sideNodes = nodesData.filter(d => d.data.centrality === 0);

  // Place the central node in the middle horizontally with slight noise
  if (centralNode) {
    centralNode.fx = width / 2;
    centralNode.fy = height / 2;
  }

  // Place the side nodes to the left and right
  if (sideNodes.length === 2) {
    sideNodes[0].x = width / 2 - 250 + (Math.random() - 0.5) * 100;
    sideNodes[0].y = height / 2 + (Math.random() - 0.5) * 100;

    sideNodes[1].x = width / 2 + 250 + (Math.random() - 0.5) * 100;
    sideNodes[1].y = height / 2 + (Math.random() - 0.5) * 100;
  }
  
  const simulation = d3.forceSimulation(nodesData)
    .force("link", d3.forceLink(linksData).distance(200).strength(1).id(d => d.data.id))
    .force("charge", d3.forceManyBody().strength(-400))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("y", d3.forceY(height / 2).strength(0.02));

  for (let i = 0; i < 300; ++i) simulation.tick(); // precompute layout

  link = svg.append("g")
    .attr("stroke", "#fff")
    .attr("stroke-opacity", 0.7)
    .attr("stroke-width", 4)
    .selectAll("line")
    .data(linksData)
    .join("line");

  // Sort by ratio, then by depth
  nodesData.sort((a, b) => {
    if (a.data.ratio === b.data.ratio) {
      return b.depth - a.depth; 
    }
    return a.data.ratio - b.data.ratio;
  });

  // Create nodes but keep them invisible initially
  node = svg.append("g")
    .selectAll("image")
    .data(nodesData)
    .join("image")
      .attr("xlink:href", d => d.data.url)
      .attr("width", d => imageSize * d.data.ratio)
      .attr("height", d => imageSize * d.data.ratio)
      .attr("x", d => d.x - (imageSize * d.data.ratio) / 2)
      .attr("y", d => d.y - (imageSize * d.data.ratio) / 2)
      .style("opacity", 0); // start hidden

  // Append <title> as separate selection
  svg.selectAll("image")
    .data(nodesData)
    .append("title")
    .text(d => d.data.name);

  svg.append("image")
    .attr("cx", width / 2)
    .attr("cy", height / 2)
    .attr("https://iiif.wellcomecollection.org/image/b16750974_l0053888.jp2/full/full/0/default.jpg");
  
  // Add spacebar event listener
  document.addEventListener('keydown', function(event) {
    // Check if spacebar was pressed and animation hasn't started yet
    if (event.code === 'Space' && !animationStarted) {
      animationStarted = true;
      startAnimation();
    }
  });

  // Start floating animation regardless
  animateFloating();
});

function startAnimation() {
  // Show first object (order=1)
  node.filter(d => d.data.order === 1)
    .transition()
    .duration(2000)
    .style("opacity", 1)
    .on("end", function() {
      // After first object is shown, show second object (order=2) after a delay
      setTimeout(() => {
        node.filter(d => d.data.order === 2)
          .transition()
          .duration(2000) //2000
          .style("opacity", 1);
      }, 1000); // 3 second delay between first and second object
    });
}
 
function cw(obj_ind) {
  return 1 - 2 * (obj_ind % 2);
}

function animateFloating() {
  const amplitude = 2.5;
  const frequency = 0.002;

  d3.timer((elapsed) => {
    node
      .attr("x", d => d.x + Math.sin(elapsed * frequency * cw(d.index) + d.index) * amplitude - (imageSize * d.data.ratio) / 2)
      .attr("y", d => d.y + Math.cos(elapsed * frequency * cw(d.index) + d.index) * amplitude - (imageSize * d.data.ratio) / 2);
  });
} 