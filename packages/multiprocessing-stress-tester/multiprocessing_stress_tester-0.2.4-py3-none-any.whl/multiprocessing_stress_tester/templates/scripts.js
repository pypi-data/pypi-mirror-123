var drawing = false;
var pause = false;
var ctx;
var line_width = 10;


function getResponse() {
	
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			alert(JSON.parse(xhttp.responseText));
		}
	};
	
	var generator = document.getElementById("generator").files[0];
	var checker = document.getElementById("checker").files[0];
	var correct = document.getElementById("correct").files[0];
	var wrong = document.getElementById("wrong").files[0];
	
	formData = new FormData();
	
	formData.append("generator", generator);
	formData.append("checker", checker);
	formData.append("correct", correct);
	formData.append("wrong", wrong);
	
	xhttp.open("POST", "sub");
	xhttp.send(formData);
	
}