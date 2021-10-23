function onRoleChange(){
  idButtonForUser = getIdButtonForUser()
  const optGroup=document.getElementById("change role")
  const formData = new FormData();
  formData.append("role",optGroup.options[optGroup.selectedIndex].text)
  formData.append("idButtonForUser",idButtoForUser)
  fetch("/change-role", {
    method: "POST",
    body: formData
  }).then(r =>location.reload())
}

function sendIdButtonForUser(value){
  sessionStorage.setItem('id_button_for_user', value.split("-")[1]);

}

function getIdButtonForUser(){
  let data = sessionStorage.getItem('id_button_for_user');

  return data
}
