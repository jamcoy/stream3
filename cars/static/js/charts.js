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
            var dataPoints = [];
            var dataPoint = {};
            $.each(response, function(index, value) {
                dataPoint = {
                    x: new Date(value.date_time),
                    y: value.price
                };
                dataPoints.push(dataPoint);
            });
            var data = [
                {
                    label: 'Fuel economy',
                    strokeColor: '#A31010',
                    data: dataPoints
                }];
            if (typeof genericChart != "undefined") {
                genericChart.destroy();
            }
            drawGenericChart(data);
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
