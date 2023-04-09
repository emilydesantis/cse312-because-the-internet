// Getting started : https://pixijs.io/guides/basics/getting-started.html
// Color palette : https://www.buffalo.edu/brand/creative/color/color-palette.html
// Text examples : https://pixijs.io/examples/#/text/text.js
// Shapes: https://pixijs.io/examples/#/graphics/simple.js
// Event listener : https://pixijs.download/dev/docs/PIXI.DisplayObject.html
// Removing containers: https://www.html5gamedevs.com/topic/30539-correct-way-to-remove-sprites-container/

//Set up the PIXI container
let app = new PIXI.Application({width: 1440, height: 810, backgroundColor: 0xffffff});
document.getElementById("main-container").appendChild(app.view);
