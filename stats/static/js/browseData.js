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
    var $yearChoice = $('#year-choice');
    var selectedYear = $yearChoice.val();
    $yearChoice.replaceWith('<span id="year-choice">' + selectedYear + '</span>');
    applyFilters(false)
});

$('.subFilter').change(function() {
    //applyFilters(true)
    console.log("Apply sub filter");
});

function applyFilters(applySubFilter){
    var filters;
    var selectedMake, selectedModel, selectedYear;
    var selectedSubModel, selectedEngine, selectedFuelType, selectedTransmission;
    var $subModelChoice = $('#sub_model-choice');
    var $engineChoice = $('#engine-choice');
    var $fuelTypeChoice = $('#fuel_type-choice');
    var $transmissionChoice = $('#transmission-choice');
    if (applySubFilter) {
        selectedMake = $('#make-choice').text();
        selectedModel = $('#model-choice').text();
        selectedYear = $('#year-choice').text();
        selectedSubModel = $subModelChoice.val();
        selectedEngine = $engineChoice.val();
        selectedFuelType = $fuelTypeChoice.val();
        selectedTransmission = $transmissionChoice.val();
        filters = { make: selectedMake,
                    model: selectedModel,
                    year: selectedYear,
                    sub_model: selectedSubModel,
                    engine: selectedEngine,
                    fuel_type: selectedFuelType,
                    transmission: selectedTransmission
        };
    } else {
        selectedMake = $('#make-choice').text();
        selectedModel = $('#model-choice').text();
        selectedYear = $('#year-choice').text();
        filters = { make: selectedMake,
                    model: selectedModel,
                    year: selectedYear
        };
    }
    $.ajax({
        url: '/stats/select_sub_details/',
        type: 'GET',
        data: filters,
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
                for (var i = 0; i < value.length; i++){
                    if (value[i].hasOwnProperty('sub_model')) {
                        if (value[i].sub_model == "") {
                            value[i].sub_model = "[None]"
                        }
                        $subModelChoice.append('<option value="' + value[i].sub_model + '">'
                                                + value[i].sub_model + ' (' + value[i].number + ')'
                                             + '</option>');
                    } else if (value[i].hasOwnProperty('cylinder_capacity')) {
                        if (value[i].cylinder_capacity == "") {
                            value[i].cylinder_capacity = "[None]"
                        }
                        $engineChoice.append('<option value="' + value[i].cylinder_capacity + '">'
                                                + value[i].cylinder_capacity + ' (' + value[i].number + ')'
                                           + '</option>');
                    } else if (value[i].hasOwnProperty('fuel_type')) {
                        if (value[i].fuel_type == "") {
                            value[i].fuel_type = "[None]"
                        }
                        $fuelTypeChoice.append('<option value="' + value[i].fuel_type + '">'
                                                + value[i].fuel_type + ' (' + value[i].number + ')'
                                             + '</option>');
                    } else if (value[i].hasOwnProperty('transmission')) {
                        if (value[i].transmission == "") {
                            value[i].transmission = "[None]"
                        }
                        $transmissionChoice.append('<option value="' + value[i].transmission + '">'
                                                    + value[i].transmission + ' (' + value[i].number + ')'
                                                 + '</option>');
                    }
                }
            });
            $subModelChoice.show();
            $engineChoice.show();
            $fuelTypeChoice.show();
            $transmissionChoice.show();
        }
    });
}