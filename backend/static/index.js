// 画面の切り替え
function showScreen(id) {
    document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

// screen-start内
let gameId = null;

function startGame(themeId){
    fetch("/game",{
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ theme_id: themeId}),
    })
    .then((response) => {
        if (!response.ok){
            throw new Error(`HTTPエラー! ステータス: ${response.status}`);
        }
        return response.json();
    })
    .then((newGameId)=>{
        gameId = newGameId;
        showScreen("screen-name");
    })
    .catch((error)=>{
        console.error("エラー:", error);
        alert("ゲームの作成に失敗しました。もう一度お試しください。");
    });
}

// screen-nameで使用

let players =[];

function createPlayer(){
    const names = [
        nameInput1 = document.getElementById("create-name1").value.trim(),
        nameInput2 = document.getElementById("create-name2").value.trim(),
        nameInput3 = document.getElementById("create-name3").value.trim()
    ];
    
    const requests = names.map((name)=>
        fetch("/player",{
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify({name: name, game_id: gameId}),
        })
        .then((response) =>{
            if (!response.ok){
                throw new Error(`HTTPエラー! ステータス: ${response.status}`);
            }
            return response.json();
        })
    );

    Promise.all(requests)
        .then((results)=>{
            players = results;
            showScreen("screen-instraction");
        })
        .catch((error) => {
            console.error("エラー", error);
            alert("プレイヤーの登録に失敗しました。もう一度お試しください。")
        });
}


// screen-instraction->screen-next-personの切り替えで使用
// 画面が切り替わったらという処理には上記のような使い方
let number = 0

// 切り替わったら動く
// plyaers[number]の名前の人を取得
// 成功したら、next-personの中に表示
// 失敗したら、alertだす

function showNextPerson(){
    const player = players[number];
    document.getElementById("next-person").textContent = `${player.name}さんへ`;
    showScreen("screen-next-person")
}
