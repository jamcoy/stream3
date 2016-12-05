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
            var label, units, unitsPosition;
            $.each(response, function(index, value) {
                if (value.hasOwnProperty('data_value')) {
                    dataPoint = {
                        x: new Date(value.date_time),
                        y: value.data_value
                    };
                    dataPoints.push(dataPoint);
                } else if (value.hasOwnProperty('units')) {
                    units = value.units;
                } else if (value.hasOwnProperty('units_position')) {
                    unitsPosition = value.units_position;
                } else if (value.hasOwnProperty('label')) {
                    label = value.label;
                }
            });
            var data = [
                {
                    label: label,
                    strokeColor: '#A31010',
                    data: dataPoints
                }];
            if (typeof genericChart != "undefined") {
                genericChart.destroy();
            }
            drawGenericChart(data, units, unitsPosition);
        }
    });
});

drawGenericChart = function (data, units, unitsPosition) {
    var canvas = $("#chart");
    canvas.css('width', $(window).innerWidth());
    canvas.css('height', $(window).innerHeight());
    var ctx3 = canvas[0].getContext('2d');
    var chartOptions = {
        bezierCurve: true,
        showTooltips: true,
        scaleShowHorizontalLines: true,
        scaleShowLabels: true,
        scaleType: "date",
        scaleDateTimeFormat: "d mmm yyyy, HH:MM"
    };
    if (unitsPosition == "before") {
        chartOptions.scaleLabel = units + "<%=value%>"
    } else {
        chartOptions.scaleLabel = "<%=value%> " + units;
    }
    genericChart = new Chart(ctx3).Scatter(data, chartOptions);
};
