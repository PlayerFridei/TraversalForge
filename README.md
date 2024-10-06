# TraversalForge
**A Comprehensive Path Traversal Payload Generator**

TraversalForge is a Python tool designed to generate path traversal payloads with various levels of complexity and encoding techniques. The tool aims to provide security researchers and penetration testers with a comprehensive suite of payloads for testing path traversal vulnerabilities on both Linux and Windows systems.

---

## Features

- Generates payloads for **Linux**, **Windows**, or **both** platforms.
- Supports multiple **encoding methods** to obfuscate payloads.
- Creates payloads in stages of **complexity**, ranging from simple traversal to advanced bypass techniques.
- Allows for customized **maximum depth** of traversal sequences.
- Outputs payloads to a specified file.

---

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/PlayerFridei/TraversalForge
    cd TraversalForge
    ```

2. **Install required packages**:
    TraversalForge requires Python 3.6+. To install the necessary packages, use the following command:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

Run the script using Python and configure your options through command-line arguments:

```bash
python traversalforge.py [OPTIONS]
```

### Command-Line Options

- **`--max-depth`** (default: `5`): Maximum number of directory traversals in a single payload.
  ```bash
  python traversalforge.py --max-depth 10
  ```

- **`--platform`** (`linux`, `windows`, `both`) (default: `both`): Specify the platform for which the payloads should be generated.
  ```bash
  python traversalforge.py --platform linux
  ```

- **`--encodings`** (default: all encodings): A list of encodings to apply to the payloads. Available encodings are:
  - `none`, `url`, `double_url`, `null_byte`, `utf16`, `hex`, `base64`, `html_entities`, `utf7`, `mixed_case`, `triple_url`, `overlong_utf8`
  
  Example:
  ```bash
  python traversalforge.py --encodings url utf16
  ```

- **`--max-payloads`** (default: `1000`): The maximum number of unique payloads to generate.
  ```bash
  python traversalforge.py --max-payloads 500
  ```

- **`--stages`** (default: `3`): The number of complexity stages for payload generation.
  ```bash
  python traversalforge.py --stages 4
  ```

- **`--output`** (default: `payloads.txt`): Output file for saving generated payloads.
  ```bash
  python traversalforge.py --output my_payloads.txt
  ```

---

## Example Usage

Generate 500 path traversal payloads for **Linux** with **maximum depth** of 7, applying **URL and double URL encoding**, and saving to `linux_payloads.txt`:
```bash
python traversalforge.py --platform linux --max-depth 7 --max-payloads 500 --encodings url double_url --output linux_payloads.txt
```

Generate 1000 payloads for **Windows and Linux** systems, with **4 stages of complexity**:
```bash
python traversalforge.py --platform both --stages 4 --max-payloads 1000
```

---

## Complexity Stages

TraversalForge generates payloads with increasing complexity across multiple stages:

1. **Stage 1 - Basic Traversals**: 
   - Simple traversal using `../` or `..\`.
   - Repeated traversals for directory depth.

2. **Stage 2 - Basic Encodings and Variants**:
   - Single-layer URL encoding.
   - Variants like `....//` and `mixed slashes`.

3. **Stage 3 - Advanced Encodings and Bypasses**:
   - Double URL encoding.
   - Unicode/UTF variants for obfuscation.
   - Null byte injection (`%00`).

4. **Stage 4 - Anti-Sanitization and Obfuscation Techniques**:
   - Fake directories and reverse sequences.
   - Windows Alternate Data Streams (`::$DATA`).
   - ASP.NET cookieless bypass patterns.

5. **Stage 5 - Mixed Encodings and Complex Patterns**:
   - Combination of URL, Unicode, and Base64 encodings.
   - Special protocol traversal (`file://`, UNC paths).

---

## Output

Generated payloads are saved to the specified output file (`payloads.txt` by default), with each payload on a new line.

Example:
```
../etc/passwd
..%2f..%2f..%2fwindows\system32\config
..%00%5cc:\inetpub\wwwroot\web.config
...
```

---

## License

TraversalForge is released under the [MIT License](LICENSE).

# Disclaimer

> Before using this software, you agree to the terms outlined in our [SECURITY.md](SECURITY.md) policy.

---

Happy hacking! 🛡️
