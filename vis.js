var ctx = document.getElementById("myChart").getContext('2d');
ctx.canvas.width  = window.innerWidth;
ctx.canvas.height = window.innerHeight;

var timeLabels = []
var requestData = []
var droppedData = []
var commonlyBlocked = {}

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
        },
        {
            data: droppedData,
            fill:false,
            borderColor: 'rgba(255, 0, 0, 1)',
            label: "Dropped Packets"
        }
        ],
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

var blockTable = document.getElementById("blockTable");
for (ip in commonlyBlocked)
{
   blockTable.insertRow(0);
   var ipCell = row.insertCell(0);
   var countCell = row.insertCell(1);

   ipCell.innerHTML = ip;
   countCell.innerHTML = commonlyBlocked[ip];
}

