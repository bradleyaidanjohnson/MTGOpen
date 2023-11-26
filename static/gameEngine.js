let phase = ["Untap", "Upkeep", "Draw", "Main 1", "Combat", "Main 2", "End"];
let deck1 = ["Plains", "Hopeful Initiate", "Plains", "Coppercoat Vanguard", "Plains", "Adeline, Resplendent Cathar", "Plains", "Recruitment Officer" , "Brutal Cathar", "Plains", "Knight-Errant of Eos", "Plains"]
let hand1 = []
document.addEventListener('DOMContentLoaded', function() {
    Init(1);
    document.querySelector('#test').innerHTML =phase[0];
    document.querySelector('#draw').addEventListener('click', function() {
        Draw(deck1, hand1);
        Hand();
    });
});

function Draw(deck, hand) {
    hand.push(deck.shift())
}

function Init(players) {
    
    for (let i = 0; i < players; i++) 
    {
        for (let i = 0; i < 7; i++) 
        {
            Draw(deck1, hand1);
        }
    }
}

function Hand() {
    document.querySelector('.hand').innerHTML = "";
    for (card in hand1) {
        document.querySelector('.hand').innerHTML += `<td><image alt="Plains" src="/static/images/cards/530155.jpg" style="max-height:100%; max-width:100%"></td>`;
    }
}
