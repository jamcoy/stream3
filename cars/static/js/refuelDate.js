$(document).ready(function(){
    $("#id_date").on('focus', function () {
        $('#id_date').daterangepicker({
            "timePicker": true,
            "timePicker24Hour": true,
            "timePickerIncrement": 15,
            "singleDatePicker": true,
            "autoApply": true,
            "locale": {
                "format": "dddd DD/MM/YYYY HH:mm"
            },
            "linkedCalendars": false,
            "startDate": moment()
        });
    });
});
