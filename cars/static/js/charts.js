var genericChart;

window.addEventListener('load', function () {
    $('.chart-select').trigger("change");
}, false);

$('.chart-select').change(function () {
    var $chartRange = $('#chart-range');
    $.ajax({
        url: '/cars/select_chart/',
        type: 'GET',
        data: {
            chart_range: $chartRange.val(),
            chart_type: $('#chart-type').val(),
            car_id: $chartRange.attr("data-id")
        },
        success: function (response) {
            var chartTitle = "Test chart title";
            var dateAxisLabels = [0, 1, 2, 3, 4, 5];
            var chartValues1 = [1, 2, 3, 4, 5, 6];
            var chartValues2 = [6, 5, 4, 3, 2, 1];
            var chartDataset = [];
            chartDataset[0] = {
                dataValues: chartValues1,
                dataLabel: "Series 1",
                dataColour: "192,192,72"
            };
            chartDataset[1] = {
                dataValues: chartValues2,
                dataLabel: "Series 2",
                dataColour: "192,72,192"
            };
            drawGenericChart(chartTitle, dateAxisLabels, chartDataset);
        }
    });
});

// accepts multiple datasets (array of objects as last parameter)
drawGenericChart = function (chartTitle, xAxisLabels, chartDataset) {

    // destroy previous chart if it exists
    if (typeof genericChart != "undefined") {
        genericChart.destroy();
    }

    var canvas = $('#chart');
    canvas.css('width', $(window).innerWidth());
    canvas.css('height', $(window).innerHeight());
    var ctx = canvas[0].getContext('2d');

    var i = 0;
    var datasetMulti = [];
    while (i < chartDataset.length) {
        var backgroundColour = "rgba(" + chartDataset[i].dataColour + ",0.4)";
        var foregroundColour = "rgba(" + chartDataset[i].dataColour + ",1)";
        datasetMulti[i] = {
            label: chartDataset[i].dataLabel,
            fill: false,
            lineTension: 0.1,
            backgroundColor: backgroundColour,
            borderColor: foregroundColour,
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: foregroundColour,
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: foregroundColour,
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: chartDataset[i].dataValues
        };
        i++;
    }

    genericChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: xAxisLabels,
            datasets: datasetMulti
        },
        options: {
            title: {
                display: true,
                text: chartTitle,
                fontSize: 18
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    }
                }]
            }
        }
    });
};