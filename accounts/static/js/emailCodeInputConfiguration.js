function checkInput(component){
    component.value=component.value.replace(/[^0-9]/g,'');
    if (component.value.length != 0){
        var currentNum = parseInt(component.id[component.id.length - 1]);
        if (currentNum != 6){
            document.getElementById(`Digit${currentNum + 1}`).focus();
        }
        else{
            document.getElementById('Confirm').focus();
        }
    }
}