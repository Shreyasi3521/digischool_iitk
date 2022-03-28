
//Adding Questions
var count = 2; //Minimum 1 question needs to be added
function addQuestion()
{
    var add = document.getElementById('question-add');
  if(add){
    if (count > 20)
    {
      alert("Not more than 20 Questions are allowed. please either merge questions or create a new test.")
      return true;
    }
    // Create a new <p> element
    var newP = document.createElement('p');
    newP.innerHTML = 'Question ' + (count);

    // Create the new text box
    var newInput = document.createElement('textarea');
    newInput.type = 'text';
    newInput.name = 'question-' + count.toString();

    var divcreate = document.createElement("div");
    divcreate.classList.add('item');

    // Add the new questions
    divcreate.appendChild(newP);
    divcreate.appendChild(newInput);
    divcreate.appendChild(document.createElement("br"))

    add.appendChild(divcreate)
    // Increment the count
    count+=1;
  }
}
