const form = document.getElementById("form-main");
const addButton = document.getElementById("add");
const submitButton = document.getElementById("create");

const csrf = document.getElementsByName('csrfmiddlewaretoken');
const url = document.URL;

form.addEventListener('submit', function(e){
    e.preventDefault();

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('title', document.getElementById('title').value);
    fd.append('description', document.getElementById('description').value);
    fd.append('linkAccess', document.getElementById('linkAccess').checked);
    fd.append('linkAccess-text-survey', document.getElementById("linkAccess-text-survey").value)

    var i = 1;
    while (document.getElementById(`question${i}`) != null){
        fd.append(`question${i}`, document.getElementById(`question${i}`).value);
        fd.append(`multichoice${i}`, document.getElementById(`multichoice${i}`).checked);
        for (var j = 1; j <= 10; ++j){
            if (document.getElementById(`answer${i}_${j}`) != null){
                fd.append(`answer${i}_${j}`, document.getElementById(`answer${i}_${j}`).value);
            }
            else{
                break;
            }
        }
        ++i;
    }

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            console.log(data.messages);
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