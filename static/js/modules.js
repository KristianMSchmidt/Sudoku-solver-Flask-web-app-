function remove_trailing_zeros(str){
    /* Simple helper function that removes insignificant trailing zeros from a sudoku string
    entered by user */
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

function show_board(sudoku, is_solution=false){
    /* Helper function that takes a soduko string and shows it on the sudoku board
    
       The sudoku is 81 string (possibly with errors input errors).
       The optional argument tells us if the given sudoku is a solved sudoku or not. 
    
        This function should do the following: 
        If sudoku is not solution 
            Draw the soduku, and make non-zero input fontweight bold.
        If solution:
            Draw the solution without changing bold fontweight 
    */        

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
}

function zero_pad(str){
    //Right pad string with zeros if it's shorter than 81 digits
    zeros = "".padStart(81 - str.length, '0');
    str += zeros;
    return str             
}

function input_handler(){
    /*This function is to be called every time the user changes the value of the input field.
      I should to do following:
        1) Tell user about possible errors in input (not digit values)
        2) Enable solve button if no errors in input
           Disable solve button if errors
        3) Draw input sudoku regardless of errors
        4) Clear solution feedback message
    */

    input = document.getElementById("custom_input").value;
    long_input = zero_pad(input);

    /* Check for errors in input (only digits are alloewed)*/
    isnum = /^\d+$/.test(input);

    if(!isnum && input.length>0){
        //There is an error in input
        document.getElementById("input_error").style.visibility="visible";
        document.getElementById("solve_btn").disabled = true;  
    }
    else{
        //No errors in input
        document.getElementById("input_error").style.visibility="hidden";   
        document.getElementById("sudoku").value = long_input;
        document.getElementById("solve_btn").disabled = false;  
    }

    //Draw board position (regardless of errors in input)
    show_board(long_input)

    //Clear feedback message
    document.getElementById("solution_feedback").innerHTML="&nbsp";
} 

function setup_custom_sudoku(sudoku){
    document.getElementById("custom_form").style.visibility="visible";
    document.getElementById("custom_input").value=remove_trailing_zeros(sudoku);
    document.getElementById("custom_input").focus();
    document.getElementById("custom_input").addEventListener('input', (event) => {
    input_handler();
    });
}

function show_succes(solved_sudoku, solution_method){
    show_board(solved_sudoku, is_solution=true); 
    document.getElementById("solution_feedback").style.color = "green";
    document.getElementById("solution_feedback").innerHTML += "Solved using " + solution_method;
}

function show_failure(){
    document.getElementById("solution_feedback").style.color = "red";
    document.getElementById("solution_feedback").innerHTML += "This sudoku has no solution!";
}