$(document).ready(function(){
    $("#id_date").on('focus', function () {
        $('#id_date').daterangepicker({
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
