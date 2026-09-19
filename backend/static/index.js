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