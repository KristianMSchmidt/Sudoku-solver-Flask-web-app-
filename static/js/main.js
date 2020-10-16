document.getElementById("sudoku4_input").focus();

document.getElementById("sudoku4_input").addEventListener('input', (event) => {
    input_handler(4);
});

function show_board(sudoku_number, sudoku, is_solution=false){
    /* sudoku_number is an integer
        sudoku is 81 string (possibly with errors)
        optional argument tells us if the given sudoku is a solution or not 
    
        This function should do the following: 
        If not solution 
            Draw the soduku, and make non-zero input fontweight bold.
        If solution:
            Draw the solution without changing bold fontweight 
        Show title of sudoku
    */
        
    //Draw sudoku 

    for (let index = 0; index < 81; index++) {
        if (sudoku[index] != "0"){
            document.getElementById(index).innerHTML = sudoku[index]
            if(!is_solution){
                document.getElementById(index).style.fontWeight = "bold";
            }
        }
        else{
            //input is 0: this only happens when input is not a solution
            document.getElementById(index).style.fontWeight = "normal";
            document.getElementById(index).innerHTML = "&nbsp";
        }
    }
    // Show title
    document.getElementById("sudoku_title").innerHTML=
            document.getElementById("title_" + sudoku_number).value;
}

function zero_pad(str){
        //right pad string with zeros if it's shorter than 81 digits
        zeros = "".padStart(81 - str.length, '0');
        str += zeros;
        return str             
    }

function input_handler(sudoku_number){
    /*This function is to be called, when user clicks "show" and every time the value og the
        sudoku input field is changed.
        1) Tell user about possible errors in input (not digit values)
        2) Enable solve button if no errors
            Disable solve button if errors
        3) Draw input sudoku regardless of errors --> use another function to do this
    */

    original_sudoku = document.getElementById("sudoku"+ sudoku_number + "_input").value;

    /* Check for errors in input */
    isnum = /^\d+$/.test(original_sudoku); //only digits are alloed 

    if(!isnum && original_sudoku.length>0){
        //There is an error in input
        document.getElementById("feedback").innerHTML = "Invalid input (only digits 0-9 allowed)"
        document.getElementById("feedback").style.color="red";      
        document.getElementById("solve_btn").disabled = true;  
    }
    else{
        //No errors in input
        document.getElementById("feedback").style.color="black";   
        document.getElementById("feedback").innerHTML="";   
        document.getElementById("solve_btn").disabled = false;  
        document.getElementById("solve_btn").addEventListener('click', (event) => {
            document.getElementById("sudoku"+sudoku_number+"_input").value=zero_pad(original_sudoku)
            document.getElementById("sudoku_form_" + sudoku_number).submit();
        });
    }

    //Draw board position (regardless of errors in input)
    show_board(sudoku_number, zero_pad(original_sudoku))
} 

function remove_trailing_zeros(str){
    let len = str.length;
    let reduced_str = str
    for (let i = 0; i < len; i++) {
        if (str[len-1-i] == 0){
            reduced_str = str.substring(0,len-1-i);
        }
        else{
            return reduced_str;
        }
    }
    return "";
}
