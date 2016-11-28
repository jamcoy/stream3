$(document).ready(function(){
    $("#id_date").on('focus', function () {
        var todaysDate = moment().format("DD\/MM\/YYYY");
        $('#id_date').daterangepicker({
            "singleDatePicker": true,
            "autoApply": true,
            "locale": {
                "format": "DD/MM/YYYY"
            },
            "linkedCalendars": false,
            "startDate": todaysDate
        }, function (start, end, label) {
            var newVar = moment(start).toJSON();
        });
    });
});
