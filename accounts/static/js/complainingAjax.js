const form = document.getElementById("form-main");

const csrf = document.getElementsByName('csrfmiddlewaretoken');
const url = document.URL;

$('#send_complaint').on('keydown', function(e){
    e.preventDefault();

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('title', document.getElementById('title').value);
    fd.append('description', document.getElementById('description').value);

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            update_messages(data.messages);
        },
        error: function(data){
            console.log("error");
        },
        cache: false,
        contentType: false,
        processData: false
    })
})

$('#send_complaint').on('click', function(e){
    e.preventDefault();

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('title', document.getElementById('title').value);
    fd.append('description', document.getElementById('description').value);

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            update_messages(data.messages);
        },
        error: function(data){
            console.log("error");
        },
        cache: false,
        contentType: false,
        processData: false
    })
})

form.addEventListener('submit', function(e){
    e.preventDefault();
})

function update_messages(messages){
    $("#div_messages").html("");
    $.each(messages, function (i, m) {
                    $("#div_messages").append("<div class='alert alert-"+m.level+"''>"+m.message+"</div>");
                });
            }

$(document).ready(function() {
    $(document).ajaxComplete(function(e, xhr, settings) {
        if (xhr.status == 278) {
            window.location.href = xhr.getResponseHeader("Location");
        }
    });
})