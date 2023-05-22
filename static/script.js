let N = document.querySelector("#nQueens").textContent;
var chessboard = document.getElementById('chessboard');
for (var i = 0; i < N; i++) {
    let div = document.createElement("div");
    for (var j = 0; j < N; j++) {
    var chessSquare = document.createElement('div');
    div.appendChild(chessSquare);
    chessSquare.className = 'chess-square';
    let pxSize = 600 / N - 2;
    chessSquare.style.width = chessSquare.style.height = pxSize + "px";
    if ((i + j) % 2 == 0) { 
        chessSquare.style.backgroundColor = '#eaebbe';
    }
    chessboard.appendChild(div);
    }
}

let arr = document.getElementById("solutionArray").textContent;
let data_arr = JSON.parse(arr)



for(let i = 0; i < data_arr.length; i++){
    let row = chessboard.children[i]
    row.children[data_arr[i]].classList.add("contains-queen")
}