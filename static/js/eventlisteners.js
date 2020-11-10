function submit(){
    document.getElementById("json_data").value = JSON.stringify(js_data);
    document.getElementById("form").submit();
}

function set_eventlisteners(){
    document.getElementById("new_sample_btn").addEventListener('click', event => {
        js_data["requested_action"] = "new_sample";
        submit();
    })
    document.getElementById("new_custom_btn").addEventListener('click', event => {
        js_data["requested_action"] = "new_custom";
        submit();
    })
    document.getElementById("solve_btn").addEventListener('click', event => {
        js_data["requested_action"] = "solve";
        submit();
    })
    document.getElementById("custom_input").addEventListener('input', event => {
        input_field_handler();
    })
}
