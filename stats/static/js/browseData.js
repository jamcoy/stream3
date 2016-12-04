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
    var element = $(this);
    var selection = element.find(":selected").val();
    element.replaceWith('<span class="frozen_option" id="' + element.attr('id') + '">' + selection + '</span>');
    applyFilters(true);
});

function applyFilters(applySubFilter){
    var filters;
    var selectedMake, selectedModel, selectedYear;
    var selectedSubModel, selectedEngine, selectedFuelType, selectedTransmission;

    var $subModelChoice = $('#sub_model-choice'),
        $engineChoice = $('#engine-choice'),
        $fuelTypeChoice = $('#fuel_type-choice'),
        $transmissionChoice = $('#transmission-choice'),
        $cars = $('#cars_sample_size'),
        $distance = $('#distance_sample_size'),
        $economy = $('#economy_calculated');

    $cars.text("");
    $distance.text("");
    $economy.text("Calculating...");

    selectedMake = $('#make-choice').text();
    selectedModel = $('#model-choice').text();
    selectedYear = $('#year-choice').text();

    if (applySubFilter) {
        if ($subModelChoice.hasClass('frozen_option')) {
            selectedSubModel = $subModelChoice.text();
        }
        if ($engineChoice.hasClass('frozen_option')) {
            selectedEngine = $engineChoice.text();
        }
        if ($fuelTypeChoice.hasClass('frozen_option')) {
            selectedFuelType = $fuelTypeChoice.text();
        }
        if ($transmissionChoice.hasClass('frozen_option')) {
            selectedTransmission = $transmissionChoice.text();
        }
        filters = { make: selectedMake,
                    model: selectedModel,
                    year: selectedYear,
                    sub_model: selectedSubModel,
                    cylinder_capacity: selectedEngine,
                    fuel_type: selectedFuelType,
                    transmission: selectedTransmission
        };
    } else {
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
            if (!$subModelChoice.hasClass('frozen_option')) {
                $subModelChoice.empty();
                $subModelChoice.append('<option>Select</option>');
            }
            if (!$engineChoice.hasClass('frozen_option')) {
                $engineChoice.empty();
                $engineChoice.append('<option>Select</option>');
            }
            if (!$fuelTypeChoice.hasClass('frozen_option')) {
                $fuelTypeChoice.empty();
                $fuelTypeChoice.append('<option>Select</option>');
            }
            if (!$transmissionChoice.hasClass('frozen_option')) {
                $transmissionChoice.empty();
                $transmissionChoice.append('<option>Select</option>');
            }

            $.each(response, function(index, value) {
                for (var i = 0; i < value.length; i++){

                    if (value[i].hasOwnProperty('sub_model')) {
                        if (!$subModelChoice.hasClass('frozen_option')) {
                            if (value[i].sub_model == "") {
                                value[i].sub_model = "[None]"
                            }
                            $subModelChoice.append('<option class="subFilter" value="' + value[i].sub_model + '">'
                                                    + value[i].sub_model + ' (' + value[i].number + ')'
                                                 + '</option>');
                        }

                    } else if (value[i].hasOwnProperty('cylinder_capacity')) {
                        if (!$engineChoice.hasClass('frozen_option')) {
                            if (value[i].cylinder_capacity == "") {
                                value[i].cylinder_capacity = "[None]"
                            }
                            $engineChoice.append('<option class="subFilter" value="' + value[i].cylinder_capacity + '">'
                                                    + value[i].cylinder_capacity + ' (' + value[i].number + ')'
                                               + '</option>');
                        }

                    } else if (value[i].hasOwnProperty('fuel_type')) {
                        if (!$fuelTypeChoice.hasClass('frozen_option')) {
                            if (value[i].fuel_type == "") {
                                value[i].fuel_type = "[None]"
                            }
                            $fuelTypeChoice.append('<option class="subFilter" value="' + value[i].fuel_type + '">'
                                                   + value[i].fuel_type + ' (' + value[i].number + ')'
                                                 + '</option>');
                        }

                    } else if (value[i].hasOwnProperty('transmission')) {
                        if (!$transmissionChoice.hasClass('frozen_option')) {
                            if (value[i].transmission == "") {
                                value[i].transmission = "[None]"
                            }
                            $transmissionChoice.append('<option class="subFilter" value="' + value[i].transmission + '">'
                                                       + value[i].transmission + ' (' + value[i].number + ')'
                                                     + '</option>');
                        }
                    } else if (value[i].hasOwnProperty('economy_calculation')) {
                        $cars.text(value[i].cars_in_sample);
                        $distance.text(value[i].distance);
                        $economy.text(value[i].economy_calculation);
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
