function addField(){
    window.event.preventDefault();
    
    // Generate a dynamic number of inputs
    // Get the element where the inputs will be added to
    var container = document.getElementById("itemList");
    
    var element = document.getElementById("listItem");
    var cloned = element.cloneNode(true);
    var del_button = cloned.querySelector("button#delbutton")

    cloned.hidden = false;
    var _id = "listItem" + container.getElementsByTagName('div').length
    cloned.id = _id
    console.log(del_button)
    del_button.setAttribute("onclick", `removeField( '${_id}')`)

    //container.appendChild(document.createElement("br"));  
    container.appendChild(cloned);
}

function removeField(elemID){
    window.event.preventDefault();
    var container = document.getElementById("itemList");
    var element = document.getElementById(elemID);
    container.removeChild(element)
}