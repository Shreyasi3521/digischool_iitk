function first_name_validation(fcheck=false)
{
    var MaxAllowed = 20;
    var name = document.forms["signupform"]["first_name"].value;
    name.trim();
    var name_len = name.length;
    var ErrorOccured = false;

    if(name_len < 1 || name_len > MaxAllowed)
    {
        ErrorOccured = true;
    }
    if (!/^[a-zA-Z]*$/g.test(name)) {
        ErrorOccured = true;
    }
    if (ErrorOccured)
    {
        if (!fcheck)
        {
            alert("First name should be 1-40 charachter long and should be alphabetic.")
            document.forms["signupform"]["first_name"].value = "";
        }
        
        return false;
    }
    return true;
}
function last_name_validation(fcheck=false)
{
    var MaxAllowed = 20;
    var name = document.forms["signupform"]["last_name"].value;
    name.trim();
    var name_len = name.length;
    var ErrorOccured = false;
    if(name_len < 1 || name_len > MaxAllowed)
    {
        ErrorOccured = true;
    }
    if (!/^[a-zA-Z]*$/g.test(name)) {
        ErrorOccured = true;
    }
    if (ErrorOccured)
    {
        if (!fcheck)
        {
            alert("Last name should be 1-40 charachter long and should be alphabetic.")
            document.forms["signupform"]["last_name"].value = "";
        }
        return false;
    }
    return true;
}

function class_validation(fcheck=false)
{
    var class_number = document.forms["signupform"]["user_class"].value;
    var ErrorOccured = false;
    class_number = parseInt(class_number);
    if (isNaN(class_number) || class_number < 1 || class_number > 12)
    {
        ErrorOccured = true;
    }
 
    if (ErrorOccured)
    {
        if (!fcheck)
        {
            alert("Class should be a number from 1-12")
            document.forms["signupform"]["user_class"].value = "";
        }
        
        return false;
    }
    return true;
}

function section_validation(fcheck=false)
{
    var section_name = document.forms["signupform"]["user_section"].value;
    var ErrorOccured = false;
    if (section_name.length != 1)
    {
        ErrorOccured = true;
    }
    section_name = section_name.toUpperCase()
    if (!(section_name === "A" ||section_name === "B" || section_name === "C" || section_name === "D" || section_name === "E" || section_name === "F"))
    {
        ErrorOccured = true;
    }
    if (ErrorOccured)
    {
        if (!fcheck)
        {
            alert("Section should be either of the following, A|B|C|D|E|F")
            document.forms["signupform"]["user_section"].value = "";
        }
        return false;
    }
    return true;
}

function rn_validation(fcheck=false)
{
    var roll_number = document.forms["signupform"]["r_number"].value;
    var ErrorOccured = false;
    roll_number_int = parseInt(roll_number);
    if (isNaN(roll_number_int) || roll_number.length < 4 || roll_number.length > 10)
    {
        ErrorOccured = true;
    }
 
    if (ErrorOccured)
    {
        if (!fcheck)
        {
            alert("Enter a valid roll number. It must be a number")
            document.forms["signupform"]["r_number"].value = "";
        }
        return false;
    }
    return true;
}

function contact_validation(fcheck=false)
{
    var contact_number = document.forms["signupform"]["contact_detail"].value;
    var ErrorOccured = false;
    contact_number_int = parseInt(contact_number);
    if (isNaN(contact_number_int) || contact_number.length < 10 || contact_number.length > 11)
    {
        ErrorOccured = true;
    }
 
    if (ErrorOccured)
    {
        if (!fcheck)
        {
            alert("Enter a valid Contact number. It must be a number without country code.")
            document.forms["signupform"]["contact_detail"].value = "";
        }
        return false;
    }
    return true;
}

function school_validation(fcheck=false)
{
    var maxAllowed = 200;
    var school_name = document.forms["signupform"]["school_name"].value;
    if(school_name.length < 10 || school_name.length > MaxAllowed)
    {
        if (!fcheck)
        {
            alert("Enter School Name. And it should be less than 200 words.")
        }
        return false;
    }
    return true;
}

function email_validation(fcheck=false)
{
    var email = document.forms["signupform"]["email_address"].value;

    if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))
     {
        if (!fcheck)
        {
            alert("Enter a valid email address!")
            document.forms["signupform"]["email_address"].value = "";
        }
        return false;
     }
     return true;
   }

function final_validation()
{
    if (first_name_validation(true) && last_name_validation(true) && class_validation(true) && section_validation(true) && rn_validation(true) && contact_validation(true) && school_validation(true) && email_validation(true))
    {
        document.forms["signupform"]["first_name"].value = document.forms["signupform"]["first_name"].value.toUpperCase()
        document.forms["signupform"]["last_name"].value = document.forms["signupform"]["last_name"].value.toUpperCase()
        document.forms["signupform"]["user_class"].value = document.forms["signupform"]["user_class"].value.toUpperCase()
        document.forms["signupform"]["school_name"].value = document.forms["signupform"]["school_name"].value.toUpperCase()
        document.forms["signupform"]["email_address"].value = document.forms["signupform"]["email_address"].value.toLowerCase()
        return true;
    }
    alert("One or more details are invalid. Please enter again!")
    return false;
    
    


}