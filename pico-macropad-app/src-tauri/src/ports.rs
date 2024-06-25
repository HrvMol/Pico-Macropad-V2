use std::fs::File;
use std::io::Read;
use serde_json::Value;

fn read_json_file(file_path: &str) -> Result<Value, Box<dyn std::error::Error>> {
    let mut file = File::open(file_path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;

    let json_value: Value = serde_json::from_str(&contents)?;

    Ok(json_value)
}

fn main() {
    let file_path = "/path/to/your/json/file.json";
    match read_json_file(file_path) {
        Ok(json_value) => {
            println!("JSON contents: {:?}", json_value);
        }
        Err(err) => {
            eprintln!("Error reading JSON file: {}", err);
        }
    }
}
 