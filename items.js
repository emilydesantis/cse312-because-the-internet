//Constants
let currentSceneID = 0; //The current scene's ID. DO NOT UPDATE THIS unless in load dialogue or container function
let currentDialogueID = 0; //The current dialogue ID. DO NOT UPDATE THIS unless in load dialogue or container function

let currentDialogue =  null; //The textbox that stores the current dialogue. Needs to be global to be able to access and remove from container
let currentDialogueSpeaker = null; //The textbox that stores the current dialogue's speaker name. Needs to be global to be able to access and remove from container

//Location of the dialogue on the screen
let dialogueLocationX = 200;
let dialogueLocationY = 700;
//Location of the speaker name on the screen
let dialogueSpeakerLocationX = 175;
let dialogueSpeakerLocationY = 590;

let nextButtonLocationX = 1270;
let nextButtonLocationY = 650;
let nextButtonWidth = 120;

//Create item methods
function createText(container, text, style, x, y) {
    const textBox = new PIXI.Text(text);
    textBox.x = x;
    textBox.y = y;
    textBox.style = style;

    container.addChild(textBox);

    return textBox;
}

function createButton(container, text, style, x, y, width, height = 70) {
    const button = new PIXI.Graphics();
    button.beginFill(0x78a547);
    button.drawRoundedRect(x, y, width, height, 10);
    button.endFill();

    const textBox = createText(container, text, style, x + 30, y + 15);

    container.addChild(button);
    button.interactive = true;
    container.addChild(textBox);
    return [button, textBox];
}



function createImage(container, image, xVal, yVal, scaling = 1, width = 0, height = 0) {
    image.x = xVal;
    image.y = yVal;
    image.scale.set(scaling)
    if (width !== 0) {
        image.width = width;
    }
    if (height !== 0) {
        image.height = height;
    }

    container.addChild(image)
}