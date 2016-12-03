$('#make-choice').change(function() {
    var selectedMake = this.value;
    $('#make-choice').replaceWith('<span id="make-choice">' + selectedMake + '</span>');
    var $modelChoice = $('#model-choice');
    $.ajax({
        url: '/stats/select_model/',
        type: 'GET',
        data: { make: selectedMake },  // data to pass to the view
        success : function(response){
            $modelChoice.empty();
            $modelChoice.append('<option>Select</option>');
            $.each(response, function(index, value) {
                $modelChoice.append('<option value="' + value.model + '">'
                                        + value.model + ' (' + value.number + ')'
                                  + '</option>');
            });
            $modelChoice.show();
        }
    });
});

$('#model-choice').change(function() {
    var selectedMake = $('#make-choice').text();
    var selectedModel = this.value;
    $('#model-choice').replaceWith('<span id="model-choice">' + selectedModel + '</span>');
    var $yearChoice = $('#year-choice');
    $.ajax({
        url: '/stats/select_year/',
        type: 'GET',
        data: { make: selectedMake,
                model: selectedModel
              },
        success : function(response){
            $yearChoice.empty();
            $yearChoice.append('<option>Select</option>');
            $.each(response, function(index, value) {
                $yearChoice.append('<option value="' + value.year + '">'
                                        + value.year + ' (' + value.number + ')'
                                 + '</option>');
            });
            $yearChoice.show();
        }
    });
});

$('#year-choice').change(function() {
    var selectedMake = $('#make-choice').text();
    var selectedModel = $('#model-choice').text();
    var selectedYear = this.value;
    $('#year-choice').replaceWith(selectedYear);
    var $subModelChoice = $('#sub_model-choice');
    var $engineChoice = $('#engine-choice');
    var $fuelTypeChoice = $('#fuel_type-choice');
    var $transmissionChoice = $('#transmission-choice');
    $.ajax({
        url: '/stats/select_sub_details/',
        type: 'GET',
        data: { make: selectedMake,
                model: selectedModel,
                year: selectedYear
              },
        success : function(response){
            $subModelChoice.empty();
            $engineChoice.empty();
            $fuelTypeChoice.empty();
            $transmissionChoice.empty();
            $subModelChoice.append('<option>Select</option>');
            $engineChoice.append('<option>Select</option>');
            $fuelTypeChoice.append('<option>Select</option>');
            $transmissionChoice.append('<option>Select</option>');

            $.each(response, function(index, value) {
                var obj = JSON.parse(value);
                if(obj[0].sub_model){
                    $subModelChoice.append('<option value="' + obj[0].sub_model + '">'
                                            + obj[0].sub_model + ' (' + obj[0].number + ')'
                                         + '</option>');
                }
                if(obj[0].cylinder_capacity){
                    $engineChoice.append('<option value="' + obj[0].cylinder_capacity + '">'
                                            + obj[0].cylinder_capacity + ' (' + obj[0].number + ')'
                                         + '</option>');
                }
                if(obj[0].fuel_type){
                    $fuelTypeChoice.append('<option value="' + obj[0].fuel_type + '">'
                                            + obj[0].fuel_type + ' (' + obj[0].number + ')'
                                         + '</option>');
                }
                if(obj[0].transmission){
                    $transmissionChoice.append('<option value="' + obj[0].transmission + '">'
                                            + obj[0].transmission + ' (' + obj[0].number + ')'
                                         + '</option>');
                }
            });
            if ($('#sub_model-choice option').length > 1) {
                $subModelChoice.show();
            }
            $engineChoice.show();
            $fuelTypeChoice.show();
            $transmissionChoice.show();
        }
    });
});