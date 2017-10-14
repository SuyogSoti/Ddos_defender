var ctx = document.getElementById("myChart").getContext('2d');
ctx.canvas.width  = window.innerWidth;
ctx.canvas.height = window.innerHeight;

var timeLabels = []
var requestData = []

//This stuff was used to generate random data. No longer needed.
/*

for (i = 0; i < 100; i++)
{
	var newstr = "10:22:" + i;
	timeLabels.push(newstr);
}

for (y = 0; y < 100; y++)
{
	var q = Math.floor((Math.random() * 10));
	if (q == 5)
	{
		requestData.push(Math.floor((Math.random() * 50)) +  50)
	}
	else
	{
		requestData.push(q);
	}
}

*/
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
    	datasets: [{
            data: requestData,
            fill: false,
            borderColor: 'rgba(153, 153, 102, 0.5)',
            pointBackgroundColor: 'rgba(153, 153, 102, 0.75)',
            label: "Requests over Time"
        }],
        labels: timeLabels
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    min: 0
                },
                scaleLabel: {
                	display: true,
                	labelString: "Requests"
                }
            }],
            xAxes: [{
            	ticks: {
            		min: 0
            	},
            	scaleLabel: {
                	display: true,
                	labelString: "Time"
                }
            }]
        }
    }
});
