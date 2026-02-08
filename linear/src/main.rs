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

fn get_argument(args: &Vec<String> ,name: &str) -> Result<String, String>{
    Err("not yet implemented".to_string())
}

fn main() {
    //collect arguments
    let args: Vec<String> = env::args().collect();

    println!("{:?}", args);
}
