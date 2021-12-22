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

function sendIdButtonForUser2(value) {
    sessionStorage.setItem('id_button_for_user', value.split("_")[1]);

}

function getIdButtonForUser() {
    let data = sessionStorage.getItem('id_button_for_user');

    return data
}


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
    var allowedExtensions =
        /(\.img)$/i; // Można dodać inne rozszerzenia plików

    let imageName = document.getElementById("image-name").value
    let imageFormat = document.getElementById("choose-image-format").value
    const loading = document.getElementById("loading-image")



    if (document.getElementById("file").files.length == 0 || imageName == null || imageName == '' || imageFormat == '') {
        alert('No files selected, format or name is too short');

    } else {
        let file = document.getElementById('file').files[0];
        loading.style.visibility = "visible"

        formData.append("file", file)
        formData.append("image-name", imageName)
        formData.append("image-format", imageFormat)

        if (!allowedExtensions.exec(file.name)) {
            alert('Invalid file type');
            return false;
        } else {
            fetch("/upload-image", {
                method: "POST",
                body: formData
            }).then(r => location.reload())
        }

    }
}

function deleteImage(buttonId) {

    const formData = new FormData();
    let idButtonForImage = buttonId.split("-")[1]

    formData.append("idButtonForImage", idButtonForImage)
    fetch("/delete_image", {
        method: "POST",
        body: formData
    }).then(r => location.reload())

}

function createArchitecture() {

    const formData = new FormData();

    const assignmentName = document.getElementById("name-assignment").value
    const assignmentDescription = document.getElementById("textarea-assignment").value
    const assignmentDatatimeEnd = document.getElementById("assignment-datatime-end").value
    const loading = document.getElementById("loading-architecture")

    loading.style.visibility = "visible"
    var radios = document.getElementsByTagName('input');
    var value = new Array(2)
    let j = 0
    for (var i = 0; i < radios.length; i++) {
        if (radios[i].type === 'radio' && radios[i].checked) {
            value[j] = radios[i].id;
            j = j + 1
        }
    }

    formData.append("assignmentName", assignmentName)
    formData.append("assignmentDescription", assignmentDescription)
    formData.append("assignmentDatatimeEnd", assignmentDatatimeEnd)
    formData.append("idGroupForArchitecture", value[0].split("-")[4])
    formData.append("idImageForArchitecture", value[1].split("-")[4])

    fetch("/create_architecture", {
        method: "POST",
        body: formData
    }).then(r => location.reload())
}

function sourceReservation() {
    const formData = new FormData();

    const reservationTime = document.getElementById("set-time").value
    let idButtonForUser = getIdButtonForUser()
    const loading = document.getElementById("loading-create-instance")
    loading.style.visibility = "visible"

    formData.append("reservationTime", reservationTime)
    formData.append("idButtonForUser", idButtonForUser)
    console.log(reservationTime)


    fetch("/resource-reservation", {
        method: "POST",
        body: formData
    }).then(r => location.reload())
}
