# Subdomain Ping Checker 🌐

A Python script that pings multiple subdomains concurrently and saves the results to a CSV file. Perfect for checking the availability of multiple websites or subdomains quickly.

## Features ✨

- **Multi-threaded pinging** for fast results
- **Cross-platform support** (Windows, Linux, macOS)
- **DNS resolution** to get IP addresses
- **CSV export** with detailed results
- **Progress tracking** with real-time updates
- **Flexible input formats** (.txt, .csv, .list files)
- **Error handling** for timeouts, DNS failures, and invalid domains
- **Wildcard domain filtering** (automatically skips `*.example.com`)
- **Smart output naming** based on input filename

## Requirements 📋

- **Python 3.6+** (no additional packages required!)
- **No external dependencies** - uses only Python standard library

### No requirements.txt needed! 🎉
This script uses only built-in Python modules, making it completely portable without any pip installations.

## Installation 🚀

1. **Install Python** (if not already installed):
   - **Windows**: Download from [python.org](https://python.org/downloads/) or install from Microsoft Store
   - **Linux**: `sudo apt install python3` (Ubuntu/Debian) or `sudo yum install python3` (CentOS/RHEL)
   - **macOS**: `brew install python3` or download from [python.org](https://python.org/downloads/)

2. **Download the script**:
   ```bash
   # Clone or download the ping_checker.py file
   # No additional installation required!
   ```

## Usage 📖

### Basic Usage

```bash
python ping_checker.py <input_file>
```

### Examples

```bash
# Check domains from a text file
python ping_checker.py domains.txt

# Check subdomains from a CSV file  
python ping_checker.py subdomains.csv

# Check websites from any supported file
python ping_checker.py my_websites.list
```

## Input File Format 📝

Create a text file with one domain per line. Supported formats:

```
# domains.txt example
https://google.com
http://github.com
stackoverflow.com
subdomain.example.com

# Comments start with # (optional)
# Empty lines are ignored

# Wildcard domains are automatically skipped
*.example.com
```

### Supported File Extensions
- `.txt` - Plain text files
- `.csv` - Comma-separated values  
- `.list` - List files

## Output Format 📊

The script generates a CSV file named `<input_filename>_ping_results.csv` with three columns:

| Subdomain | Status | IP Address |
|-----------|--------|------------|
| google.com | ACTIVE | 142.250.191.14 |
| github.com | ACTIVE | 140.82.114.4 |
| nonexistent.example.com | NO RESPONSE (DNS Failed) | Cannot Resolve |
| *.example.com | SKIPPED (Wildcard) | N/A |

### Status Types

- **ACTIVE** - Domain responds to ping
- **NO RESPONSE (Ping Failed)** - Domain resolves but doesn't respond to ping  
- **NO RESPONSE (DNS Failed)** - Domain name doesn't resolve
- **NO RESPONSE (Timeout)** - Request timed out
- **SKIPPED (Wildcard)** - Contains wildcards (*) and was skipped
- **ERROR** - Unexpected error occurred

## Examples 🎯

### Example 1: Basic Domain Check

**Input file** (`websites.txt`):
```
https://google.com
https://github.com  
https://stackoverflow.com
badexample12345.com
```

**Command**:
```bash
python ping_checker.py websites.txt
```

**Output**:
```
Subdomain Ping Checker - Fixed Version
==================================================
Input file: websites.txt
Output file: websites_ping_results.csv
Python version: 3.11.0
Platform: Windows
Current directory: C:\Users\YourName\Scripts
==================================================
Loading domains from websites.txt...
Found 4 domains to check

Starting ping checks...
This may take a while depending on the number of domains.
------------------------------------------------------------
[  1/  4] ( 25.0%) ✓ google.com                           -> ACTIVE
[  2/  4] ( 50.0%) ✓ github.com                           -> ACTIVE  
[  3/  4] ( 75.0%) ✓ stackoverflow.com                    -> ACTIVE
[  4/  4] (100.0%) ✗ badexample12345.com                  -> NO RESPONSE (DNS Failed)

Results saved to: websites_ping_results.csv

==================================================
SUMMARY
==================================================
Total domains checked: 4
Active (responding): 3
No response: 1
Errors: 0
Skipped (wildcards): 0
==================================================

First few active domains:
  ✓ google.com -> 142.250.191.14
  ✓ github.com -> 140.82.114.4
  ✓ stackoverflow.com -> 151.101.193.69

Total execution time: 2.34 seconds

Press Enter to exit...
```

### Example 2: Large Subdomain List

For checking many subdomains (100+), the script automatically uses multi-threading:

```bash
python ping_checker.py large_subdomain_list.txt
```

The script will process up to 10 domains simultaneously for faster results.

## Command Line Help 💡

If you run the script without arguments or with wrong arguments, it shows usage instructions:

```bash
python ping_checker.py
```

Output:
```
Error: Incorrect number of arguments!

Subdomain Ping Checker - Usage Instructions
==================================================
Usage:
  python script.py <input_file>
  python script.py domains.txt
  python script.py subdomains.txt

Input file format:
  - One subdomain per line
  - Supported formats:
    https://example.com
    http://subdomain.example.com
    subdomain.example.com
    # Comments start with # (optional)

Supported file extensions: .txt, .csv, .list
==================================================
```

## Troubleshooting 🔧

### Common Issues

1. **"Python was not found"**
   ```bash
   # Try these alternatives:
   py ping_checker.py domains.txt
   python3 ping_checker.py domains.txt
   ```

2. **"File not found"**
   - Make sure the input file is in the same directory as the script
   - Check the filename spelling and extension

3. **"No valid domains found"**
   - Verify your file contains valid domain names
   - Check file encoding (should be UTF-8)
   - Make sure domains are one per line

4. **All domains show "NO RESPONSE"**
   - You might be behind a restrictive firewall
   - Try testing with well-known domains like `google.com`
   - Some networks block ICMP (ping) traffic

### Getting Better Results

- **Corporate Networks**: Many corporate firewalls block ping traffic
- **Home Networks**: Usually work fine with most domains  
- **VPN/Proxy**: May affect ping results
- **DNS Issues**: Script will show "DNS Failed" for domains that can't be resolved

## Performance 📈

- **Single domain**: ~1-3 seconds
- **10 domains**: ~3-5 seconds  
- **100 domains**: ~10-30 seconds (depending on network)
- **1000+ domains**: Several minutes (uses 10 concurrent threads)

## Supported Platforms 🖥️

- ✅ **Windows 10/11**
- ✅ **Linux** (Ubuntu, CentOS, etc.)
- ✅ **macOS**
- ✅ **Windows Subsystem for Linux (WSL)**

## Contributing 🤝

Feel free to submit issues, feature requests, or pull requests!

## License 📄

This project is open source and available under the [MIT License](LICENSE).

---

**Happy domain checking!** 🎉

For questions or issues, please create an issue in the repository.
