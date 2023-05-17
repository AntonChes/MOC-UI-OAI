// send form by press 'Enter' on active textarea
$('#wrapper_Form textarea.user_input').keypress(function (e) {
    if(e.which === 13 && !e.shiftKey) {
        e.preventDefault();
    
        $(this).closest("form").submit();
    }
});


// open aside menu - model config
$(".gear-btn").click(function(){
    if( $("#modelConfigSection").css('display') == 'none') {
        $("#modelConfigSection").animate({"width": "406px",}, 200);
        // $("#modelConfigSection").css({"display": "block"});
        $("#modelConfigSection").animate({ "opacity": "show",}, 500);

        $(this).css({"background": "#32394B", "border": "1px solid #32394B"});
        $(".gear-btn svg g path").attr("stroke", "#FFF");

    } else {
        $("#modelConfigSection").animate({ "opacity": "hide",}, 300);
        // $("#modelConfigSection").css({"display": "none"});
        $("#modelConfigSection").animate({"width": "0px",}, 500);

        $(this).css({"background": "#FFF", "border": "1px solid #FFF"});
        $(".gear-btn svg g path").attr("stroke", "#32394B");
    }

    // check if block overflowed, and add/remove bottom shadow
    setTimeout(function (){
        var el_bott = $('div.mconfigs-list div div.shadow--bottom')
        var el_top = $('div.mconfigs-list div div.shadow--top')

        if ($('.mconfigs-content').get(0).offsetHeight < $('.mconfigs-content').get(0).scrollHeight) {
            // overflow
            console.log(true);
            el_bott.css({"display": "block", "opacity": "2.72227"});
            el_top.css({"opacity": "0"});
        } else {
            // doesn't overflow
            el_bott.css({"opacity": "0"});
            el_top.css({"opacity": "0"});
            console.log(false);
        }         
      }, 250); 

});

// open/close dropdown with radio btn
$(".dropdown-select").click(function(){
    console.log($(this).hasClass('.active-dr'));
    if($(this).hasClass('active-dr') == false) {
        $(this).children(".arrow-close").css({"transform": "rotate(180deg)"});
        $(this).children(".arrow-close").css({"display": "none"});
        $(this).children(".arrow-open").css({"display": "block"});
        $(this).addClass('active-dr');
        $(this).parent().find('.dropdown-body').addClass('show-dr');
        $(".black-wrp").css({"display": "block"});
    } else {
        $(this).children(".arrow-close").css({"transform": "rotate(0deg)"});
        $(this).children(".arrow-close").css({"display": "block"});
        $(this).children(".arrow-open").css({"display": "none"});
        $(this).removeClass('active-dr');
        $(this).parent().find('.dropdown-body').removeClass('show-dr');  
        $(".black-wrp").css({"display": "none"});
    }
});

// close all windows, wraper click
$(".black-wrp").click(function(){
    $(this).css({"display": "none"});
    $('#wrapper').find('.dropdown-body').removeClass('show-dr');
    $('#wrapper').find('.dropdown-select').removeClass('active-dr');
    $('#wrapper').find('.arrow-close').css({"transform": "rotate(0deg)"});
    $('#wrapper').find('.arrow-close').css({"display": "block"});
    $('#wrapper').find('.arrow-open').css({"display": "none"});
});

// onchange for raiobtn | Change input value, when dropdown is open and radio butn checked
$('input[type="radio"]').on('change', function() {
    var radio_val = $(this).attr('value');
    var radio_title = $(this).attr('id');
    console.log(radio_val, radio_title);
    $(this).parent().parent().parent().find('.dropdown-select input').attr('value', radio_title);
    $(this).parent().parent().parent().find('.dropdown-select input').attr('data-val', radio_val);
});
