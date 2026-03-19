function checkLink(){
let url = document.getElementById("url").value;

if(!url){
document.getElementById("result").innerText = "❌ Enter a link first";
return;
}

fetch("/check", {
method: "POST",
headers: {"Content-Type": "application/x-www-form-urlencoded"},
body: "url=" + encodeURIComponent(url)
})
.then(res => res.text())
.then(data => {
document.getElementById("result").innerText = data;
});
}


function validateForm(){
let url = document.getElementById("url").value;

if(!url){
alert("Please paste a video link!");
return;
}

document.forms[0].submit();
}