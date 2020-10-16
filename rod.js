function remove_trailing_zeros(str){
    let len = str.length;
    let reduced_str = str
    for (let i = len; i < len; i++) {
        if (str[len-1-i] == 0){
            reduced_str = str.substring(0,len-1-i);
        }
        else{
            return reduced_str;
        }
    }
    return "";
}

console.log(remove_trailing_zeros(""))

