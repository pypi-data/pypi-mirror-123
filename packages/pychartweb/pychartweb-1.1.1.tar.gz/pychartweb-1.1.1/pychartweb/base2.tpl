<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>PY GRAPH</title>
	<script src='/chart.js'></script>
</head>
<body>
% for i in graph:
<center>
<div style="height: 500px; width:500px">
  <canvas id="{{i['base']['name']}}" width="100" height="100"></canvas>
  </div>
</center>
<script>
var ctx = document.getElementById("{{i['base']['name']}}").getContext('2d');
var mixedChart = new Chart(ctx, {
    data: {
        datasets: {{!i['data']}},
        labels: {{!i['base']['xaxis']}}
    },
});
</script>
 
% end
</body>
</html>