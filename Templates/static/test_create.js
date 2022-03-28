function printfiles(){
    var x = document.getElementById("selectedfiles");
    console.log("ran")
    var output = "Uploaded files,<br>";
    if ('files' in x) {
        if (x.files.length == 0) {
            output = "Select one or more files.";
        } else {
        for (var i = 0; i < x.files.length; i++) {
            var file = x.files[i];
            if ('name' in file) {
                output += file.name + "<br>";
            }
        }
        }
    }
    else {
        x.setAttribute(value="None") //to check if it is correct or not
        output += "Either no files were uploaded or Some files types are not supported.";
        output  += "<br>The path of the selected file: " + x.value;
    }
    document.getElementById("filesplaceholder").innerHTML = output;
}