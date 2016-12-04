Chart.defaults.global.responsive = true;
Chart.defaults.global.animation = true;
var genericChart;

window.addEventListener('load', function () {
    $('#chart-range').trigger("change");
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
            var data = [
                {
                    label: 'Fuel economy',
                    strokeColor: '#A31010',
                    data: [
                        {
                            x: new Date('2016-04-11T11:45:00'),
                            y: 29.3
                        },
                        {
                            x: new Date('2016-04-20T12:51:00'),
                            y: 28.4
                        },
                        {
                            x: new Date('2016-04-30T14:10:00'),
                            y: 33.1
                        },
                        {
                            x: new Date('2016-05-24T15:15:00'),
                            y: 30.0
                        },
                        {
                            x: new Date('2016-06-05T17:00:00'),
                            y: 29.7
                        },
                        {
                            x: new Date('2016-06-21T21:00:00'),
                            y: 32.3
                        },
                        {
                            x: new Date('2016-07-01T13:00:00'),
                            y: 32.5
                        }
                    ]
                }];
            if (typeof genericChart != "undefined") {
                genericChart.update();
            } else {
                drawGenericChart(data);
            }
        }
    });
});

drawGenericChart = function (data) {
    var canvas = $("#chart");
    canvas.css('width', $(window).innerWidth());
    canvas.css('height', $(window).innerHeight());
    var ctx3 = canvas[0].getContext('2d');
    genericChart = new Chart(ctx3).Scatter(data, {
        bezierCurve: true,
        showTooltips: true,
        scaleShowHorizontalLines: true,
        scaleShowLabels: true,
        scaleType: "date",
        scaleLabel: "<%=value%> MPG"
    });
};
