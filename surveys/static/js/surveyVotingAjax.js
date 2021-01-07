const form_rating = document.getElementById("form-rating");
const form_lock = document.getElementById("form-lock");

const csrf = document.getElementsByName('csrfmiddlewaretoken');
const url = document.URL;

const button_lock = document.getElementById('lock_btn');
const button_like = document.getElementById('like_btn');
const button_dislike = document.getElementById('dislike_btn');

function check(){
    var btn = document.getElementById('vote_btn');
    var i = 0;

    var flag = true;
    while (document.getElementsByName(`answers_inp${i + 1}`).length != 0){
        var answers = document.getElementsByName(`answers_inp${i + 1}`);
        var localFlag = false;
        for (var index = 0; index < answers.length; ++index){
            if (answers[index].checked == true){
                localFlag = true;
                break;
            }
        }
        flag = (flag && localFlag);
        ++i;
    }
    if (flag){
        if (btn.hasAttribute('disabled')){
            btn.removeAttribute('disabled');
        }
    }
    else{
        if (!btn.hasAttribute('disabled')){
            btn.setAttribute('disabled', '');
        }
    }
}

$('#like_btn').on('keydown', function(e){
    e.preventDefault();

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('rating_change', '1');

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            update_buttons(data.btn_change, data.count_like, data.count_dislike);
        },
        error: function(data){
            console.log("error");
        },
        cache: false,
        contentType: false,
        processData: false
    })
})

$('#like_btn').on('click', function(e){
    e.preventDefault();

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('rating_change', '1');

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            update_buttons(data.btn_change, data.count_like, data.count_dislike);
        },
        error: function(data){
            console.log("error");
        },
        cache: false,
        contentType: false,
        processData: false
    })
})

$('#dislike_btn').on('keydown', function(e){
    e.preventDefault();

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('rating_change', '-1');

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            update_buttons(data.btn_change, data.count_like, data.count_dislike);
        },
        error: function(data){
            console.log("error");
        },
        cache: false,
        contentType: false,
        processData: false
    })
})

$('#dislike_btn').on('click', function(e){
    e.preventDefault();

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('rating_change', '-1');

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            update_buttons(data.btn_change, data.count_like, data.count_dislike);
        },
        error: function(data){
            console.log("error");
        },
        cache: false,
        contentType: false,
        processData: false
    })
})

$('#lock_btn').on('keydown', function(e){
    e.preventDefault();

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('change_lock', '1');

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            update_lock_btn(data.btn_change);
        },
        error: function(data){
            console.log("error");
        },
        cache: false,
        contentType: false,
        processData: false
    })
})

$('#lock_btn').on('click', function(e){
    e.preventDefault();

    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('change_lock', '1');

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            update_lock_btn(data.btn_change);
        },
        error: function(data){
            console.log("error");
        },
        cache: false,
        contentType: false,
        processData: false
    })
})

function update_lock_btn(to){
    if (to == '1'){
        button_lock.value = 'Lock';
    }
    else{
        button_lock.value = 'Unlock';
    }
}

function update_buttons(state, count_like, count_dislike){
    console.log(state);
    if (state == '1'){
        button_like.value = `Like (${count_like})`;
        button_like.style = "background-color: rgb(50, 255, 50);";
        button_dislike.value = `Dislike (${count_dislike})`;
        button_dislike.style = "background-color: white;";
    }
    else if (state == '0'){
        button_like.value = `Like (${count_like})`;
        button_like.style = "background-color: white;";
        button_dislike.value = `Dislike (${count_dislike})`;
        button_dislike.style = "background-color: white;";
    }
    else{
        button_like.value = `Like (${count_like})`;
        button_like.style = "background-color: white;";
        button_dislike.value = `Dislike (${count_dislike})`;
        button_dislike.style = "background-color: rgb(255, 50, 50);";
    }
}

form_rating.addEventListener('submit', function(e){
    e.preventDefault();
})

form_lock.addEventListener('submit', function(e){
    e.preventDefault();
})