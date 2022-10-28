function getQueryParam(param, defaultValue = '') {
    location.search.substr(1)
        .split("&")
        .some(function (item) { // returns first occurence and stops
            return item.split("=")[0] == param && (defaultValue = item.split("=")[1], true)
        })
    return defaultValue
}
var payload = {
    'lp_s1': getQueryParam('s1'),
    'lp_s2': getQueryParam('s2'),
    'lp_s3': getQueryParam('s3'),
    'lp_s4': getQueryParam('s4'),
    'lp_s5': getQueryParam('s5'),
    'child_under_18':'',
    'brand':'',
    'asd_diagnosis':'',
    'description':'',
    'firstname':'',
    'lastname':'',
    'email':'',
    'phonenumber':'',
    'universal_leadid':'',
    'trusted_form_cert_id':'',
    'leadid_tcpa_disclosure':'',
}


$(document).ready(function() {

    $("#checkcompensation").click(function() {
        $([document.documentElement, document.body]).animate({
            scrollTop: $("#form").offset().top
        }, 500);
    });






$("#asd_diagnosis").focus(function(e){

    $("#asd_diagnosis").removeClass("error");
    $("#asd_diagnosis_error").html("");

});


$("#brand").focus(function(e){

    $("#brand").removeClass("error");
    $("#brand_error").html("");

});
$("#child_under").focus(function(e){

    $("#child_under").removeClass("error");
    $("#child_under_error").html("");

});


$("#first_name").focus(function(e){
    $("#first_name").removeClass("error");
    $("#first_name_error").html("");

});
$("#last_name").focus(function(e){
    $("#last_name").removeClass("error");
    $("#last_name_error").html("");
});
$("#phone_number").focus(function(e){
    $("#phone_number").removeClass("error");
    $("#phone_number_error").html("");
});
$("#email_address").focus(function(e){
    $("#email_address").removeClass("error");
    $("#email_address_error").html("");
});

$('#leadid_tcpa_disclosure').change(function() {
    if(this.checked) {
        $('#leadid_tcpa_disclosure_error').html("");
        $("#leadid_tcpa_disclosure_label").removeClass("error");

    }

});

/*
$( "#formsubmit" ).click(function() {
  $( "form" ).submit();
});
 */
let form_submitting = false;

$("form").submit(function(e) {
    e.preventDefault();

    var valid = true;
    if ($("#asd_diagnosis").val() === "") {
        $("#asd_diagnosis").addClass("error");
        $("#asd_diagnosis_error").html("Please select an option");
        valid = false;
    }


    if ($("#child_under").val() === "") {
        $("#child_under").addClass("error");
        $("#child_under_error").html("Please select an option");
        valid = false;
    }

    if ($("#brand").val() === "") {
        $("#brand").addClass("error");
        $("#brand_error").html("Please select a brand");
        valid = false;
    }
    if ($("#first_name").val() === "") {

        $("#first_name").addClass("error");
        $("#first_name_error").html("Please enter your first name");
        valid = false;
    }

    if ($("#last_name").val() === "") {
        $("#last_name").addClass("error");
        $("#last_name_error").html("Please enter your last name");
        valid = false;
    }

    if ($("#phone_number").val() === "") {
        $("#phone_number").addClass("error");
        $("#phone_number_error").html("Please enter your phone number");
        valid = false;
    }
    if ($("#email_address").val() === "") {
        $("#email_address").addClass("error");
        $("#email_address_error").html("Please enter your email address");
        valid = false;
    }
    var phoneNumber = $("#phone_number").val().replace(/\D/g, '');
    if((phoneNumber.length !=10 ) && (phoneNumber.length != 11)){
        $("#phone_number").addClass("error");
        $("#phone_number_error").html("Please enter a valid phone number");
        valid = false;
        console.log(phoneNumber.length);
    }


    var validEmailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if (!$('#email_address').val().match(validEmailRegex) && $('#email_address').val() != '') {
        $("#email_address").addClass("error");
        $("#email_address_error").html("Please enter a valid email address");
        valid = false;
    }

    if(valid == true) {
        var data = new FormData();
        data.append('lp_s1', getQueryParam('s1'));
        data.append('lp_s2', getQueryParam('s2'));
        data.append('lp_s3', getQueryParam('s3'));
        data.append('lp_s4', getQueryParam('s4'));
        data.append('lp_s5', getQueryParam('s5'));
        data.append('firstname', $('#first_name').val());
        data.append('lastname', $('#last_name').val());
        data.append('email', $('#email_address').val());
        data.append('phonenumber', $('#phone_number').val());
        data.append('description', $("#description").val());
        data.append('universal_leadid', $('#leadid_token').val());
        data.append('trusted_form_cert_id', $('input[name=xxTrustedFormCertUrl]').val());
        data.append('leadid_tcpa_disclosure', $('#leadid_tcpa_disclosure').val());
        data.append('child_under_18', $('#child_under').val());
        data.append('brand', $('#brand').val());
        data.append('asd_diagnosis', $('#asd_diagnosis').val());

        if (!form_submitting){
            form_submitting = true;
            $.ajax({
                type: 'post',
                url: '/api/submitform2',
                dataType: 'json',
                processData: false,
                contentType: false,
                data: data,
                success: function (response, status, xhr) {
                    form_submitting = false;
                    if (!response.error) {
                        window.location.replace("/success");
                    } else {
                        window.location.replace("/complete");
                        console.log(response)
                    }
                    // window.location.replace("/complete");
                },
                error: function (response, status, xhr) {
                    form_submitting = false;
                    window.location.replace("/complete");
                }
            });
         }
    }


});



});
