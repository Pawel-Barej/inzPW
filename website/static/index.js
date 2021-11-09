function onRoleChange() {
    let idButtonForUser = getIdButtonForUser()
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
            list[i] = checkboxes[i].value
        }
    }
    formData.append("check", list)

    fetch("/add-user-to-group", {
        method: "POST",
        body: formData
    }).then(r => location.reload())

}


function createGroup() {
    let nameForGroup = document.getElementById("name-for-group").value;
    const formData = new FormData();
    formData.append("nameForGroup", nameForGroup)

    fetch("/create-group", {
        method: "POST",
        body: formData
    }).then(r => location.reload())

}

function tableGroupWithUsers() {
    let nameGroup = document.getElementById("select-table-group-with-users").value;
    window.location.href = `/manage-groups/${nameGroup}`

}

function uploadImage() {
    const formData = new FormData();
    let file = document.getElementById('file').files[0];
    console.log(file)
    formData.append("file", file)


    fetch("/create-assignments", {
        method: "POST",
        body: formData
    }).then()

}

