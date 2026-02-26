//todo
//get arguments +
//validate arguments +
//  all requied arguments given +
//  keys must be coprime +
//  input exist +
//get input text +
//encrypt/decrypt input text
//  since this cipher only operates on alphabet letters
//  non-alphabet characters will be ignored
//write the output text
use std::{char, env};
use std::path::Path;
use std::fs;

pub static ALPHABET: [char; 26] = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z'
];
struct Options {
    a:i32,
    b:i32,
    input_path:String,
    output_path:String,
    input_text:String,
    output_text:String,
    encrypt: bool,
}

//wtf
//this language is strange
pub fn get_char(index: i32) -> Option<char> {
    if (0..26).contains(&index) {
        return ALPHABET.get(index as usize).copied();
    } else {
        return None;
    }
}

pub fn index_of(c: char) -> Option<usize> {
    let mut i = 0;
    while i < 26 {
        if c == ALPHABET[i] {
            return Some(i);
        }
        i += 1;
    }
    None
}

/*
    function returns a reference to a string after a string that matches name or
    an error if not found 
*/

fn get_argument<'res>(args: &'res [String] ,name: &str) -> Result<&'res String, String>{
    let mut i = 0;
    while i < args.len() {
        if args[i] == name && i+1 < args.len(){
            return Ok(&args[i+1]);
        }
        i += 1;
    };
    return Err(format!("argument '{}' not found",&name).to_string());
}

//function checks if argument with that name exist
fn has_argument(args: &[String], name:&str) -> bool {
    if args.contains(&name.to_string()){
        return true;
    }
    return false;
}

fn gcd(a: i32, b: i32) -> i32 {
    let mut x = a;
    let mut y = b;

    while y != 0 {
        let r = x % y;
        x = y;
        y = r;
    }

    x
}

/*
    function takes an input from the console, validates it
    and writes it to the struct or throws an error
*/

fn get_input(args: &[String], opt: &mut Options) -> Result<(), String>{
    // validating A and B
    let a_str = get_argument(&args, "-a")?.clone();
    let b_str = get_argument(&args, "-b")?.clone();

    //this is so ugly
    opt.a = a_str.parse::<i32>().map_err(|_| format!("incorrect value A: {}, expected whole number",a_str))?;
    opt.b = b_str.parse::<i32>().map_err(|_| format!("incorrect value B: {}, expected whole number",a_str))?;

    if gcd(opt.a, opt.b) != 1 {
        return Err("arguments A and B are not coprime".to_string());
    }

    //validating paths
    let input_path = get_argument(&args, "--input")?;
    let output_path = get_argument(&args, "--output")?;

    let p=Path::new(&input_path);
    if !p.exists() {
        return Err(format!("file '{}' does not exist",input_path));
    }
    opt.input_path = input_path.clone();
    opt.output_path = output_path.clone();

    //reading input
    opt.input_text = fs::read_to_string(&input_path)
    .map_err(|_| "an error occured when trying to read input file")?;

    //reading encryption/decryption mode
    if has_argument(&args, "-e"){
        opt.encrypt = true
    } else if has_argument(&args, "-d"){
        opt.encrypt = false
    } else {
        return Err("no flag for encryption/decryption mode (-e/-d)".to_string())
    }

    Ok(())
}

/*
    this is the de facto cryptographic function
    i will use the same one for encryption/decryption
    just with diffrent keys
*/

fn modify_char(c:&char, a:&i32, b:&i32) -> Option<char>{
    //this language is confusing
    let index = index_of(*c)? as i32;

    let newIndex = index*a + b;

    return get_char(newIndex);
}

/*
    this function applies cryptographic function to every char
    or omits if char not in alphabet
*/

fn modify_string(input:String, a:i32, b:i32, encrypt:bool) -> String {
    for c in input.chars() {

    }
    return  "TwojaStara".to_string();
}

fn main() -> Result<(),String>{
    let mut options:Options = Options
    { a: 0,
    b: 0,
    input_path: "".to_string(),
    output_path: "".to_string(),
    input_text: "".to_string(),
    output_text: "".to_string(),
    encrypt: true
    };

    let args: Vec<String> = env::args().collect();

    //assign values from args to variables

    //get_argument(&args, "jeremiasz")?;
    get_input(&args, &mut options)?;
    println!("{:?}", args);

    Ok(())
}
