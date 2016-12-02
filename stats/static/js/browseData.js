$('.carMakeSelection').on('click', function(event){
    event.preventDefault();
    var element = $(this); // element is the clicked button in this example
    $.ajax({
        url: '/stats/test_ajax/',
        type: 'GET',
        data: { make: element.attr("data-id")},  // data to pass to the view
        success : function(response){
            alert(response);
        }
    })
});
