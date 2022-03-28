const formId = "submitform"; // ID of the form
const url = location.href; //  href for the page
const formIdentifier = `${url} ${formId}`; // Identifier used to identify the form
const saveButton = document.querySelector("#save"); // select save button
const alertBox = document.querySelector(".alert"); // select alert display div
let form = document.querySelector(`#${formId}`); // select form
let formElements = form.elements; // get the elements in the form



const getFormData = () => {
    let data = { [formIdentifier]: {} }; // create an empty object with the formIdentifier as the key and an empty object as its value
    for (const element of formElements) {
      if (element.name.length > 0) {
        data[formIdentifier][element.name] = element.value;
      }
    }
    return data;
};
  
saveButton.onclick = event => {
    event.preventDefault();
    data = getFormData();
    localStorage.setItem(formIdentifier, JSON.stringify(data[formIdentifier]));
    const message = "Answers are saved.";
    displayAlert(message);
};
  

const displayAlert = message => {
    alertBox.innerText = message; // add the message into the alert box
    alertBox.style.display = "block"; // make the alert box visible
    setTimeout(function() {
      alertBox.style.display = "none"; // hide the alert box after 1 second
    }, 1000);
};

const populateForm = () => {
    if (localStorage.key(formIdentifier)) {
      const savedData = JSON.parse(localStorage.getItem(formIdentifier)); // get and parse the saved data from localStorage
      for (const element of formElements) {
        if (element.name in savedData) {
          element.value = savedData[element.name];
        }
      }
      const message = "Saved Answers loaded.";
      displayAlert(message);
    }
  };
  document.onload = populateForm(); // populate the form when the document is loaded