//Create welcome screen container

function initializeLobbyContainer(){
    const lobbyContainer = new PIXI.Container();
    //Welcome screen items
    const lobbyText = createText(lobbyContainer, "Welcome To My Lobby, Bitch", headingStyle, 280, 300);
    const [startButton, startText] = createButton(lobbyContainer, "Start Game", regularButtonStyle, 600, 500, 200);

//Start button event listener
//updated this to load the new container I created which falls in between welcome and consultation containers
    startButton.on("pointerup", (event) => {
        //initializeDoctorIntroductionContainer();
    });
    loadContainer(lobbyContainer);
}
initializeLobbyContainer();