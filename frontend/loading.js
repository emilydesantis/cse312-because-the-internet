"use strict";

function loadContainer(container) {
    // https://www.html5gamedevs.com/topic/30539-correct-way-to-remove-sprites-container/
    app.stage.removeChildren();
    app.stage.addChild(container);
}