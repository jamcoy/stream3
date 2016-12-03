$('#make-choice').change(function() {
    var selectedMake = this.value;
    $.ajax({
        url: '/stats/select_model/',
        type: 'GET',
        data: { make: selectedMake },  // data to pass to the view
        success : function(response){
            var $modelChoice = $('#model-choice');
            $modelChoice.empty();
            $modelChoice.append('<option>Select</option>')
            $.each(response, function(index, value) {
                $modelChoice.append('<option value="' + value.model + '">'
                                        + value.model + ' (' + value.number + ')'
                                  + '</option>');
            });
        }
    });
});

$('#model-choice').change(function() {
    var selectedMake = $('#make-choice').val();
    var selectedModel = this.value;
    $.ajax({
        url: '/stats/select_year/',
        type: 'GET',
        data: { make: selectedMake,
                model: selectedModel
              },
        success : function(response){
            var $yearChoice = $('#year-choice');
            $yearChoice.empty();
            $yearChoice.append('<option>Select</option>')
            $.each(response, function(index, value) {
                $yearChoice.append('<option value="' + value.year + '">'
                                        + value.year + ' (' + value.number + ')'
                                 + '</option>');
            });
        }
    });
});