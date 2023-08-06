function getResponse() {
	
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			alert("Submission completed! id = " + JSON.parse(xhttp.responseText)['id']);
		}
	};
	
	var generator = document.getElementById("generator").files[0];
	var checker = document.getElementById("checker").files[0];
	var correct = document.getElementById("correct").files[0];
	var wrong = document.getElementById("wrong").files[0];
	var testcase = document.getElementById("testcase").value;
	var timelimit = document.getElementById("timelimit").value;
	var safety = document.getElementById("safety").value;
	
	formData = new FormData();
	
	formData.append("testcase", testcase);
	formData.append("timelimit", timelimit);
	formData.append("safety", safety);
	formData.append("generator", generator);
	formData.append("checker", checker);
	formData.append("correct", correct);
	formData.append("wrong", wrong);
	
	xhttp.open("POST", "sub");
	xhttp.send(formData);
	
}

function reqSubmissions(page) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			
			showSubmissions(JSON.parse(xhttp.responseText)['rows']);
		}
	};
	
	formData = new FormData();
	
	formData.append("page", page);
	
	xhttp.open("POST", "showRows");
	xhttp.send(formData);

}

function createDownload(fileName, fileStr) {
	
	var downloadEl = document.createElement('a'); 
	downloadEl.href = 'data:attachment/text,' + encodeURIComponent(fileStr);
	downloadEl.text = "Download " + fileName;
	downloadEl.target = '_blank';
	downloadEl.download = fileName;
	return downloadEl;
	
}

function showSubmissions(rows) {
	var result = "<table border=\"2\"><tr><th>ID</th><th>Generator</th><th>Checker</th><th>Correct</th><th>Wrong</th><th>Debugger Result</th></tr>";
	var rows = rows;
	for (i = 0; i < rows.length; i++){
		result += "<tr><td>";
		
		result += rows[i][0].toString(); // 0 ID
		result += "</td><td>";
		
		result += createDownload('generator.cpp', rows[i][1]).outerHTML; // 1 Generator
		result += "</td><td>";
		
		result += createDownload('checker.cpp', rows[i][2]).outerHTML; // 2 Checker
		result += "</td><td>";
		
		result += createDownload('correct.cpp', rows[i][3]).outerHTML; // 3 Correct
		result += "</td><td>";
		
		result += createDownload('wrong.cpp', rows[i][4]).outerHTML; // 4 Wrong
		result += "</td><td>";
		
		result += rows[i][5].toString(); // 5 Debugger Result
		result += "</td></tr>";
	}
	
	result += "</table>";
	document.getElementById('submissionRows').innerHTML = result;
}
