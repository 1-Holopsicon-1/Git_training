const form = document.getElementById("form-main");

const csrf = document.getElementsByName('csrfmiddlewaretoken');
const url = document.URL;

$('#reject').on('keydown', function(e){
    e.preventDefault();

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('reject', '1');

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            console.log("success");
        },
        error: function(data){
            console.log("error");
        },
        cache: false,
        contentType: false,
        processData: false
    })
    window.location.replace("complaints");
})

$('#reject').on('click', function(e){
    e.preventDefault();

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('reject', '1');

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            console.log("success");
        },
        error: function(data){
            console.log("error");
        },
        cache: false,
        contentType: false,
        processData: false
    })
    window.location.replace("complaints");
})

$('#accept').on('keydown', function(e){
    e.preventDefault();

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('verdict', document.getElementById('verdict').value);
    if (document.getElementById('verdict').value == 'Temporary ban' || document.getElementById('verdict').value == 'Temporary right limit'){
        fd.append('switch-input', document.getElementById('switch-input').checked);
        if (document.getElementById('switch-input').checked){
            fd.append('until-time', document.getElementById('until-time-inp').value);
        }
        else{
            fd.append('for-time', document.getElementById('for-time-inp').value);
        }
    }

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            console.log("success");
        },
        error: function(data){
            console.log("error");
        },
        cache: false,
        contentType: false,
        processData: false
    })
    window.location.replace("complaints");
})

$('#accept').on('click', function(e){
    e.preventDefault();

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('verdict', document.getElementById('verdict').value);
    if (document.getElementById('verdict').value == 'Temporary ban' || document.getElementById('verdict').value == 'Temporary right limit'){
        fd.append('switch-input', document.getElementById('switch-input').checked);
        if (document.getElementById('switch-input').checked){
            fd.append('until-time', document.getElementById('until-time-inp').value);
        }
        else{
            fd.append('for-time', document.getElementById('for-time-inp').value);
        }
    }

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            console.log("success");
        },
        error: function(data){
            console.log("error");
        },
        cache: false,
        contentType: false,
        processData: false
    })
    window.location.replace("complaints");
})

form.addEventListener('submit', function(e){
    e.preventDefault();
})

$(document).ready(function() {
    var date = new Date();
    date.setDate(new Date().getDate()+1)
    document.getElementById("until-time-inp").setAttribute('min', date.toISOString().split('T')[0]);
})