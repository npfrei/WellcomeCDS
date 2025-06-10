// Constants
const width = 960;
const height = 600;
const imageSize = 100;
const animationDuration = 2000; // in ms
const animationDelay = 1000;    // in ms

// Global variables
let link, node;
let nodesData = [], linksData = [];
let animationStarted = false;

// Initialize SVG container
const svg = d3.select("#chart")
  .attr("viewBox", [0, 0, width, height]);

/**
 * Calculates direction multiplier for floating animation
 * @param {number} objIndex - Index of the object
 * @return {number} Direction multiplier (1 or -1)
 */
function calculateDirection(objIndex) {
  return 1 - 2 * (objIndex % 2);
}

/**
 * Handles the floating animation of nodes
 */
function animateFloating() {
  const amplitude = 2.5;
  const frequency = 0.001;
  
  d3.timer((elapsed) => {
    node
      .attr("x", d => {
        const oscillation = Math.sin(elapsed * frequency * calculateDirection(d.index) + d.index) * amplitude;
        return d.x + oscillation - (imageSize * d.data.ratio) / 2;
      })
      .attr("y", d => {
        const oscillation = Math.cos(elapsed * frequency * calculateDirection(d.index) + d.index) * amplitude;
        return d.y + oscillation - (imageSize * d.data.ratio) / 2;
      });
  });
}

/**
 * Starts the sequence animation when triggered by spacebar
 */
function startAnimation() {
  // Show first object (order=1)
  node.filter(d => d.data.order === 1)
    .transition()
    .duration(animationDuration)
    .style("opacity", 1)
    .on("end", function() {
      // After first object is shown, show second object (order=2) after a delay
      setTimeout(() => {
        node.filter(d => d.data.order === 2)
          .transition()
          .duration(animationDuration)
          .style("opacity", 1);
      }, animationDelay); // delay between first and second object
    });
}

/**
 * Sets up keyboard event listeners
 */
function setupEventListeners() {
  document.addEventListener('keydown', function(event) {
    // Check if spacebar was pressed and animation hasn't started yet
    if (event.code === 'Space' && !animationStarted) {
      animationStarted = true;
      startAnimation();
    }
  });
}

/**
 * Positions nodes in the layout
 * @param {Object} centralNode - The central node in the graph
 * @param {Array} sideNodes - Array of side nodes
 */
function positionNodes(centralNode, sideNodes) {
  // Place the central node in the middle
  if (centralNode) {
    centralNode.fx = width / 2;
    centralNode.fy = height / 2;
  }
  
  // Position side nodes to the left and right with some randomness
  if (sideNodes && sideNodes.length === 2) {
    const randomOffset = () => (Math.random() - 0.5) * 100;
    
    sideNodes[0].x = width / 2 - 250 + randomOffset();
    sideNodes[0].y = height / 2 + randomOffset();
    
    sideNodes[1].x = width / 2 + 250 + randomOffset();
    sideNodes[1].y = height / 2 + randomOffset();
  }
}

/**
 * Creates the force simulation for node layout
 * @param {Array} nodes - Array of node data
 * @param {Array} links - Array of link data
 * @return {Object} D3 force simulation
 */
function createForceSimulation(nodes, links) {
  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).distance(200).strength(1).id(d => d.data.id))
    .force("charge", d3.forceManyBody().strength(-400))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("y", d3.forceY(height / 2).strength(0.02));
  
  // Precompute layout
  for (let i = 0; i < 300; ++i) {
    simulation.tick();
  }
  
  return simulation;
}

/**
 * Renders the graph links
 * @param {Array} links - Array of link data
 */
function renderLinks(links) {
  return svg.append("g")
    .attr("stroke", "#fff")
    .attr("stroke-opacity", 0.7)
    .attr("stroke-width", 4)
    .selectAll("line")
    .data(links)
    .join("line");
}

/**
 * Renders the graph nodes
 * @param {Array} nodes - Array of node data
 * @return {Object} D3 selection of nodes
 */
function renderNodes(nodes) {
  // Sort nodes by ratio, then by depth for proper layering
  nodes.sort((a, b) => {
    if (a.data.ratio === b.data.ratio) {
      return b.depth - a.depth; 
    }
    return a.data.ratio - b.data.ratio;
  });
  
  // Create nodes but keep them invisible initially
  const nodeSelection = svg.append("g")
    .selectAll("image")
    .data(nodes)
    .join("image")
      .attr("xlink:href", d => d.data.url)
      .attr("width", d => imageSize * d.data.ratio)
      .attr("height", d => imageSize * d.data.ratio)
      .attr("x", d => d.x - (imageSize * d.data.ratio) / 2)
      .attr("y", d => d.y - (imageSize * d.data.ratio) / 2)
      .style("opacity", 0); // start hidden
  
  // Add tooltips
  svg.selectAll("image")
    .data(nodes)
    .append("title")
    .text(d => d.data.name);
  
  return nodeSelection;
}

/**
 * Main initialization function
 */
function initialize() {
  Promise.all([
    d3.json("aids.json")
  ]).then(([data]) => {
    // Create hierarchy and extract nodes and links
    const root = d3.hierarchy(data);
    linksData = root.links();
    nodesData = root.descendants();
    
    // Find special nodes
    const centralNode = nodesData.find(d => d.data.centrality === 1);
    const sideNodes = nodesData.filter(d => d.data.centrality === 0);
    
    // Position nodes in layout
    positionNodes(centralNode, sideNodes);
    
    // Create simulation
    createForceSimulation(nodesData, linksData);
    
    // Render links and nodes
    link = renderLinks(linksData);
    node = renderNodes(nodesData);
    
    
    // Setup event listeners and animations
    setupEventListeners();
    animateFloating();
  }).catch(error => {
    console.error("Error loading data:", error);
  });
}

// Start the application
initialize();