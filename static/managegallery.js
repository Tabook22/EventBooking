//check to see if the selection option is chenged or not, and if it changed go the delallsections button and change its href
//we do this to make sure that when we click the second delete button in the popup modal the proper link to the delete_all page contains all the needed information
$('#selevent').on('change', function (e) {
    $("#post-form").trigger('submit');
    $('#allimg')
        .empty(); //clear all images to show only the images in the selected image gallery collection.

    //get the selected item text and add it to the delete link
    var valueSelected = this.value;
    newUrl = "/videos/delete_all/" + valueSelected
    $("#delallsections").attr("href", newUrl);
});

//here when we select options from the dropdown list and we search for the image collections associated with that 
//image gallery collection
$('#post-form').submit(function (e) {
    var selev = $('#selevent option:selected').val(); // get the selected value
    $('#allimg')
        .empty(); //clear all images to show only the images in the selected image gallery collection.
    if (selev == 0) {
        //if we are at the first image collection means we didn't choosed any image collection yet
        e.preventDefault(); //stop form from submitting, no data will be submitted
        $('#envinfo').append(
            '<span style="color:red;">Sorry!. Please Select the Gallery Event </span>'
        ); // display error message
    }
});

//if delete all is clicked we want to make sure the user selected an image gallery collection to be fully deleted
$('#deleteall').on('click', function (e) {
    let selev = $('#selevent option:selected').val() //get the select option value
    let selet = $('#selevent option:selected').text() //get the selected option text
    $("#getselcol").text(selet); // to display it in the info section

    //if the selected value is the first value in the selection menue then abort
    if (selev == 0) {
        e.preventDefault(); //stop form from submitting
        $('#envinfo').empty();
        $('#envinfo').append('<span style="color:red;">Sorry!. Please Select the Gallery Event </span>');
    } else {
        $("#delmsg_wrapper").css("display", "flex");
    }
});

$("#delallsections").on('click', function (e) {
    // the delete all button will send a request to server first , then it will call the hide()function
    //the map function will return an array of values
    var selected_val = $.map($("input[name='d_name']:checked"), function (a) {
        return a.value;
    }).join(" "); // join and put whitespace between each element in the array
    let getname = selected_val;
    // The link url 
    newUrl = "/videos/delete_all/" + getname
    //{% url 'delete-all' getname %}
    $("#delallsections").attr("href", newUrl);
    hide();
});
$("#canceldel").click(function () {
    hide();
});

function hide() {
    $("#delmsg_wrapper").css("display", "none");

}

//check box for images check all box at onec all togather
$('#select_all').on('click', function () {
    if (this.checked) {
        $('.checkbox').each(function () {
            this.checked = true;
        });
    } else {
        $('.checkbox').each(function () {
            this.checked = false;
        });
    }
});

$('.checkbox').on('click', function () {
    if ($('.checkbox:checked').length == $('.checkbox').length) {
        $('#select_all').prop('checked', true);
    } else {
        $('#select_all').prop('checked', false);
    }
});