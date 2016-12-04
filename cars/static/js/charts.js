var $chartRange = $('#chart-range'),
    $chartType = $('#chart-type'),
    $chartDiv = $('#chart'),
    chartClass = $('.chart-select');

chartClass.change(function () {
    var temp = $chartRange.val() + ", " + $chartType.val();
    $chartDiv.text(temp);
});
