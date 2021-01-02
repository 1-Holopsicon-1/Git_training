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