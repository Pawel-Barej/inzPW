function onRoleChange() {
    idButtonForUser = getIdButtonForUser()
    const optGroup = document.getElementById("change role")
    const formData = new FormData();

    formData.append("role", optGroup.options[optGroup.selectedIndex].text)
    formData.append("idButtonForUser", idButtonForUser)
    fetch("/change-role", {
        method: "POST",
        body: formData
    }).then(r => location.reload())
}

function sendIdButtonForUser(value) {
    sessionStorage.setItem('id_button_for_user', value.split("-")[1]);

}

function getIdButtonForUser() {
    let data = sessionStorage.getItem('id_button_for_user');

    return data
}

//---------------------------------------------------

function onAddToGroup() {
    list = []
    idButtonForUser = getIdButtonForUser()
    const formData = new FormData();
    formData.append("idButtonForUser", idButtonForUser)
    var checkboxes = document.getElementsByTagName("input");
    console.log(checkboxes)
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].type == "checkbox" && checkboxes[i].checked) {
            console.log(checkboxes[i].value)
            list[i] = checkboxes[i].value
        }
    }
    formData.append("check", list)
    console.log(checkboxes.length)
    console.log(list[0])



    fetch("/add-user-to-group", {
        method: "POST",
        body: formData
    }).then(r => location.reload())

}

