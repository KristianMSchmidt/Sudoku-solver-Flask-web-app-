// Make input sudoku visible on board
show_board();        

// If current sudoku is a custom sudoku, set this up:
if (js_data["title"] == 'Your Sudoku'){
    setup_custom_sudoku()
}

// After a solution attempt, do the following
if (js_data["requested_action"] == "solve"){
    if (js_data["is_solvable"]){
        show_succes()
    } 
    else {
        show_failure()
    }
}

// Set global eventlisteners
set_eventlisteners();