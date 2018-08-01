$(document).ready(function() {
	console.log(chart_id[0]);
	$('#Temperature').highcharts({
		chart: chart[0],
		title: title[0],
		xAxis: xAxis[0],
		yAxis: yAxis[0],
		series: series[0]
	});
});