const form_rating = document.getElementById('form-rating');
const form_lock = document.getElementById("form-lock");
const form_comments = document.getElementById("form-comments");

console.log(form_rating);

const csrf = document.getElementsByName('csrfmiddlewaretoken');
const url = document.URL;

const button_lock = document.getElementById('lock_btn');
const button_like = document.getElementById('like_btn');
const button_dislike = document.getElementById('dislike_btn');

var activeIndex = -1;

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
        button_dislike.style = "background-color: #2E8BC0;";
    }
    else if (state == '0'){
        button_like.value = `Like (${count_like})`;
        button_like.style = "background-color: #2E8BC0;";
        button_dislike.value = `Dislike (${count_dislike})`;
        button_dislike.style = "background-color: #2E8BC0;";
    }
    else{
        button_like.value = `Like (${count_like})`;
        button_like.style = "background-color: #2E8BC0;";
        button_dislike.value = `Dislike (${count_dislike})`;
        button_dislike.style = "background-color: rgb(255, 50, 50);";
    }
}

form_rating.addEventListener("submit", function(e){
    e.preventDefault();
})

$("#form-lock").on('submit', function(e){
    e.preventDefault();
})

$("form-comments").on('submit', function(e){
    e.preventDefault();
})

function createReplyBox(index, reply_index, user_link, user_name, creationTime){
    deleteReplyBox();
    var parent = document.getElementById(`commentReplySection_${index}`);
    var replyInfo = document.createElement("label");
    replyInfo.id = `commentReplyInfo_${index}`;
    replyInfo.innerHTML = "Reply to ";
    var a = document.createElement("a");
    a.id = `commentReplyLink_${index}`;
    a.href = user_link;
    a.innerHTML = user_name;
    var deleteBtn = document.createElement("input");
    deleteBtn.id = `commentReplyDelete_${index}`;
    deleteBtn.type = "button";
    deleteBtn.value = "Delete";
    deleteBtn.setAttribute("onclick", "deleteReplyBox()");
    var timeL = document.createElement("label");
    timeL.id = `commentReplyTime_${index}`;
    timeL.innerHTML = "(" + creationTime + ")";
    var br = document.createElement("br");
    br.id = `commentReplyBr_${index}`;
    var txt = document.createElement("textarea");
    txt.id = `commentReplyTextarea_${index}`;
    txt.setAttribute("oninput", `updateSendBtn(this, 'commentReplySend_${index}')`);
    txt.rows = 2;
    txt.cols = 50;
    txt.style = "resize: none;";
    var sendbtn = document.createElement("input");
    sendbtn.id = `commentReplySend_${index}`;
    sendbtn.type = "submit";
    sendbtn.setAttribute("disabled", "true");
    sendbtn.value = "Send";
    parent.appendChild(replyInfo);
    parent.appendChild(a);
    parent.appendChild(timeL);
    parent.appendChild(deleteBtn);
    parent.appendChild(br);
    parent.appendChild(txt);
    clickattr = "event.preventDefault();sendComment(" + reply_index.toString() + ", " + txt.id.toString() + ");";
    sendbtn.setAttribute("onclick", clickattr);
    parent.appendChild(sendbtn);
    activeIndex = index;
}

function deleteReplyBox(){
    if (activeIndex != -1){
        var parent = document.getElementById(`commentReplySection_${activeIndex}`);
        var replyInfo = document.getElementById(`commentReplyInfo_${activeIndex}`)
        var a = document.getElementById(`commentReplyLink_${activeIndex}`);
        var deleteBtn = document.getElementById(`commentReplyDelete_${activeIndex}`);
        var timeL = document.getElementById(`commentReplyTime_${activeIndex}`);
        var br = document.getElementById(`commentReplyBr_${activeIndex}`);
        var txt = document.getElementById(`commentReplyTextarea_${activeIndex}`);
        var sendbtn = document.getElementById(`commentReplySend_${activeIndex}`);
        parent.removeChild(replyInfo);
        parent.removeChild(a);
        parent.removeChild(deleteBtn);
        parent.removeChild(timeL);
        parent.removeChild(br);
        parent.removeChild(txt);
        parent.removeChild(sendbtn);
        activeIndex = -1;
    }
}

function updateSendBtn(textarea, id){
    var button = document.getElementById(id);
    if (textarea.value.length > 0){
        if (button.hasAttribute("disabled"))
            button.removeAttribute("disabled");
    }
    else
        button.setAttribute("disabled", "true");
}

function sendComment(id, text){
    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf[0].value);
    fd.append('answered', id);
    fd.append('text', text.value);

    $.ajax({
        type: 'POST',
        url: url,
        enctype: 'multipart/form-data',
        data: fd,
        success: function(data){
            
        },
        error: function(data){
            
        },
        cache: false,
        contentType: false,
        processData: false
    })
}

$(document).ready(function() {
    console.log("redirected");
    $(document).ajaxComplete(function(e, xhr, settings) {
        if (xhr.status == 278) {
            window.location.href = xhr.getResponseHeader("Location");
            console.log("redirected");
        }
    });
})