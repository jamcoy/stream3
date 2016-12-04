$(document).ready(function(){
    var $date = $("#id_date")
    $date.on('focus', function () {
        $date.daterangepicker({
            "timePicker": true,
            "timePicker24Hour": true,
            "timePickerIncrement": 15,
            "singleDatePicker": true,
            "autoApply": true,
            "locale": {
                "format": "YYYY-MM-DD HH:mm:ss"
            },
            "linkedCalendars": false,
            "startDate": moment()
        });
    });
});
