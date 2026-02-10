//todo
//get arguments
//validate arguments
//  all requied arguments given
//  keys must be coprime
//  input exist
//get input text
//encrypt/decrypt input text
//  since this cipher only operates on alphabet letters
//  non-alphabet characters will be ignored
//write the output text
use std::env;
use std::path::Path;
use std::fs;

struct Options {
    a:i32,
    b:i32,
    input_path:String,
    output_path:String,
    input_text:String,
    output_text:String,
    encrypt: bool,
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
    return Err(format!("argument \"{}\" not found",&name).to_string());
}

//function checks if argument with that name exist
fn has_argument(args: &[String], name:&str) -> bool {
    if args.contains(&name.to_string()){
        return true;
    }
    return false;
}

fn get_input(args: &[String], opt: &mut Options) -> Result<(), String>{
    // validating A and B
    let a_str = get_argument(&args, "-a")?.clone();
    let b_str = get_argument(&args, "-b")?.clone();

    //this is so ugly
    opt.a = a_str.parse::<i32>().map_err(|_| format!("incorrect value A: {}, expected whole number",a_str))?;
    opt.b = b_str.parse::<i32>().map_err(|_| format!("incorrect value B: {}, expected whole number",a_str))?;

    //validating paths
    let input_path = get_argument(&args, "--input")?;
    let output_path = get_argument(&args, "--output")?;

    let p=Path::new(&input_path);
    if !p.exists() {
        return Err(format!("file {} does not exist",input_path));
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
