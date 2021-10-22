function onRoleChange(){
  idButton = getIdButton()
  const optGroup=document.getElementById("change role")
  const formData = new FormData();
  formData.append("role",optGroup.options[optGroup.selectedIndex].text)
  formData.append("idButton",idButton)
  fetch("/change-role", {
    method: "POST",
    body: formData
  }).then(r =>location.reload())
}

function sendIdButton(value){
  sessionStorage.setItem('id_button', value.split("-")[1]);

}

function getIdButton(){
  let data = sessionStorage.getItem('id_button');

  return data
}
