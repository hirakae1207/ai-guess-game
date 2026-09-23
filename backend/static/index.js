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
        document.getElementById("create-name1").value.trim(),
        document.getElementById("create-name2").value.trim(),
        document.getElementById("create-name3").value.trim(),
        document.getElementById("create-name4").value.trim()
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
        .then(() => {
            return fetch(`/assignment?game_id=${gameId}`,{
                method: "POST",
            });
        })
        .then((res) => {
            if(!res.ok){
                throw new Error(`HTTPエラー! ステータス: ${res.status}`);
            }
            return res.json();
        })
        .then((assignedPlayers) => {
            players = assignedPlayers;
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

// screen-next-person->screen-keywordで使用
function showKeyword(){
    const player = players[number];
    // document.getElementById("player's_theme").textContent = `${player.assigned_topic_id}`;
    fetch(`/player/topic/${player.id}`,{
    // fetch("/player/topic/"{
        method: "GET",
        headers: {"Content-Type": "application/json"},
        // body: JSON.stringify({player_id: player.id}),
    })
    .then((response) =>{
        if (!response.ok){
            throw new Error(`HTTPエラー! ステータス: ${response.status}`);
        }
        return response.json();
    })
    .then((topic)=>{
        document.getElementById("player_theme").textContent=topic.topic_text
        showScreen("screen-keyword")
    })
    .catch((error)=>{
        console.error("エラー", error);
        alert("取得に失敗しました。もう一度お試しください。")
    })
}

// screen-keywordで使用
function createKeyword(){
    const keyword = document.getElementById("create-keyword").value.trim();
    const player = players[number];

    fetch(`/player/keyword?player_id=${player.id}`,{
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({keyword: keyword})
    })
    .then((response) =>{
        document.getElementById("create-keyword").value = "";
        if (!response.ok){
            return response.json().then((data) => {
                throw new Error(data.detail || `HTTPエラー! ステータス: ${response.status}`);
            });
        }
        document.getElementById("create-keyword").value = "";
        return response.json();
    })
    .then(()=>{
        number++;
        if(number < 4){
            showNextPerson();
        }
        else{
            showScreen("screen-result");
            getTopic().then(()=>{
            getKeyword();
            sendAI();
            });
        }
    })
    .catch((error) => {
        console.error("エラー:", error);
        alert(error.message);
    });
}



function sendAI(){
    fetch(`/judge?game_id=${gameId}`,{
        method:"POST",
    })
    .then((response)=>{
        if(!response.ok){
            throw new Error(`HTTPエラー! ステータス: ${response.status}`);
        }
        return response.json();
    })
    .then((result)=>{
        document.getElementById("AI_judge").textContent=result.response;
    })
    .catch((error) => {
        console.error("エラー:", error);
        alert("キーワードの送信に失敗しました。もう一度お試しください。");
    });
}

// function getTopicByGame(){
//     fetch(`/player/topic_id/${gameId}`,{
//         method:"GET",
//     })
//     .then((response)=>{
//         if(!response.ok){
//             throw new Error(`HTTPエラー ステータス: ${response.status}`);
//         }
//         return response.json();
//     })
//     .then((result)=>{
//         document.getElementById("topic").textContent=result
//     })
//     .catch((error) => {
//         console.error("エラー:", error);
//         alert("キーワードの送信に失敗しました。もう一度お試しください。");
//     });
// }
// let theme = null;

// function getTheme(){
//     fetch(`/game/theme?game_id=${gameId}`,{
//         method:"GET",
//         headers: {"Content-Type": "application/json"}
//     })
//     .then((response) =>{
//         if (!response.ok){
//             throw new Error(`HTTPエラー! ステータス: ${response.status}`);
//         }
//         return response .json();
//     })
//     .then((result) =>{
//         theme = result;
//     })
//     .catch((error) => {
//         console.error("エラー:", error);
//         alert("取得に失敗しました。もう一度お試しください。");
// });
// }

let topic1_id =null;
let topic2_id = null;


function getTopic(){
    return fetch(`/game/topic?game_id=${gameId}`,{
        method: "GET",
        headers: {"Content-Type": "application/json"}
    })
    .then((response) =>{
        if(!response.ok){
            throw new Error(`HTTPエラー! ステータス: ${response.status}`);
        }
        return response.json();
    })
    .then((result)=>{
        topic1_id = result[0].id
        topic2_id = result[1].id
        document.getElementById("topic1").textContent=`topic1: ${result[0].topic_text}`;
        document.getElementById("topic2").textContent=`topic2: ${result[1].topic_text}`;
    })
    .catch((error) => {
        console.error("エラー:", error);
        alert("取得に失敗しました。もう一度お試しください。")
    });
}

function getKeyword() {
  const topicIds = [topic1_id, topic2_id];

  const requests = topicIds.map((topicId) =>
    fetch(`/keyword/${topicId}?game_id=${gameId}`).then((response) => {
      if (!response.ok) {
        throw new Error(`HTTPエラー! ステータス: ${response.status}`);
      }
      return response.json();
    })
  );

  Promise.all(requests)
    .then((results) => {
      const keywordDiv = document.getElementById("keyword");
      keywordDiv.innerHTML = "";

      results.forEach((topicGroup) => {
        topicGroup.forEach((row) => {
          const p = document.createElement("p");
          p.textContent = `${row.name}さん: ${row.keyword}`;
          keywordDiv.appendChild(p);
        });
      });
    })
    .catch((error) => {
      console.error("エラー:", error);
      alert("キーワードの取得に失敗しました。もう一度お試しください。");
    });
}



// function getKeyword(){
//     fetch(`/keyword/${game_ai}`,{
//         method: "GET",
//         headers: {"Content-Type": "application/json"}
//     })
//     .then((response)=>{
//         if(!response.ok){
//             throw new Error(`HTTPエラー! ステータス: ${response.status}`);
//         }
//         return response.json();
//     })
//     .then((result)=>{
//         const keyword1 = result[0].keyword
//         const keyword2 = result[1].keyword
//         const keyword3 = result[2].keyword
//     })
//     .catch((error)=>{
//         console.error("エラー:", error)
//         alert("取得に失敗しました。もう一度お試しください。")
//     })
// }