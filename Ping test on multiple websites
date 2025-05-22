#!/usr/bin/env python3
"""
Subdomain Ping Checker - Fixed Version
Pings a list of subdomains and saves results to CSV file
"""

import subprocess
import csv
import socket
import platform
import re
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def extract_domain_from_url(url):
    """Extract domain name from URL"""
    url = url.strip()
    # Remove http:// or https://
    if url.startswith(('http://', 'https://')):
        url = re.sub(r'^https?://', '', url)
    
    # Remove path if present
    domain = url.split('/')[0]
    
    return domain

def ping_domain(domain, timeout=3):
    """
    Ping a domain and return status and IP
    Returns: (status, ip_address)
    """
    # Skip wildcard domains
    if '*' in domain:
        return 'SKIPPED (Wildcard)', 'N/A'
    
    try:
        # First try to resolve the domain to get IP
        try:
            ip_address = socket.gethostbyname(domain)
        except socket.gaierror:
            return 'NO RESPONSE (DNS Failed)', 'Cannot Resolve'
        
        # Determine ping command based on OS
        if platform.system().lower() == 'windows':
            ping_cmd = ['ping', '-n', '1', '-w', str(timeout * 1000), domain]
        else:
            ping_cmd = ['ping', '-c', '1', '-W', str(timeout), domain]
        
        # Execute ping command
        try:
            result = subprocess.run(
                ping_cmd, 
                capture_output=True, 
                text=True, 
                timeout=timeout + 2,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system().lower() == 'windows' else 0
            )
            
            if result.returncode == 0:
                return 'ACTIVE', ip_address
            else:
                return 'NO RESPONSE (Ping Failed)', ip_address
        except subprocess.TimeoutExpired:
            return 'NO RESPONSE (Timeout)', ip_address
            
    except Exception as e:
        return f'ERROR: {str(e)}', 'Unknown'

def process_single_domain(domain_url):
    """Process a single domain and return result"""
    domain = extract_domain_from_url(domain_url)
    
    if not domain:
        return domain_url, 'ERROR (Invalid Domain)', 'N/A'
    
    status, ip = ping_domain(domain)
    return domain, status, ip

def load_domains_from_file(filename):
    """Load domains from file, filtering out empty lines"""
    # Check if file exists (additional check)
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        print(f"Please make sure the file exists in the current directory: {os.getcwd()}")
        return None
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            domains = []
            invalid_lines = []
            
            for line_num, line in enumerate(file, 1):
                original_line = line
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Check if line looks like a domain/URL
                if line.startswith('http') or '.' in line:
                    domains.append(line)
                else:
                    invalid_lines.append((line_num, original_line.strip()))
            
            # Show invalid lines if any
            if invalid_lines:
                print(f"\nWarning: Found {len(invalid_lines)} invalid lines in '{filename}':")
                for line_num, line_content in invalid_lines[:5]:  # Show first 5
                    print(f"  Line {line_num}: {line_content}")
                if len(invalid_lines) > 5:
                    print(f"  ... and {len(invalid_lines) - 5} more")
                print("These lines will be skipped.\n")
            
            if not domains:
                print(f"Error: No valid domains found in '{filename}'")
                print("Make sure your file contains domains in these formats:")
                print("  https://example.com")
                print("  http://subdomain.example.com")
                print("  subdomain.example.com")
                return None
                
            return domains
            
    except UnicodeDecodeError:
        print(f"Error: Cannot read file '{filename}' - appears to be a binary file or wrong encoding.")
        print("Please make sure it's a text file with UTF-8 encoding.")
        return None
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return None

def save_results_to_csv(results, filename='subdomain_ping_results.csv'):
    """Save results to CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['Subdomain', 'Status', 'IP Address'])
            
            # Write results
            for domain, status, ip in results:
                writer.writerow([domain, status, ip])
                
        print(f"\nResults saved to: {filename}")
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False

def print_summary(results):
    """Print summary of results"""
    total = len(results)
    active = sum(1 for _, status, _ in results if status == 'ACTIVE')
    no_response = sum(1 for _, status, _ in results if 'NO RESPONSE' in status)
    errors = sum(1 for _, status, _ in results if 'ERROR' in status)
    skipped = sum(1 for _, status, _ in results if 'SKIPPED' in status)
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Total domains checked: {total}")
    print(f"Active (responding): {active}")
    print(f"No response: {no_response}")
    print(f"Errors: {errors}")
    print(f"Skipped (wildcards): {skipped}")
    print("="*50)

def show_usage():
    """Show usage instructions"""
    print("--- Tool by Mohd Abdul Jameel ---")
    
    print("Subdomain Ping Checker - Usage Instructions")
    print("="*50)
    print("Usage:")
    print("  python script.py <input_file>")
    print("  python script.py domains.txt")
    print("  python script.py subdomains.txt")
    print()
    print("Input file format:")
    print("  - One subdomain per line")
    print("  - Supported formats:")
    print("    https://example.com")
    print("    http://subdomain.example.com") 
    print("    subdomain.example.com")
    print("    # Comments start with # (optional)")
    print("    ")
    print("Supported file extensions: .txt, .csv, .list")
    print("="*50)

def validate_input_file(filename):
    """Validate input file format and existence"""
    # Check if filename is provided
    if not filename:
        return False, "No filename provided"
    
    # Check file extension
    valid_extensions = ['.txt', '.csv', '.list']
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext not in valid_extensions:
        return False, f"Invalid file extension '{file_ext}'. Supported: {', '.join(valid_extensions)}"
    
    # Check if file exists
    if not os.path.exists(filename):
        return False, f"File '{filename}' not found"
    
    # Check if file is readable
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read(100)  # Read first 100 chars to test
        return True, "File is valid"
    except Exception as e:
        return False, f"Cannot read file: {e}"

def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Error: Incorrect number of arguments!")
        print()
        show_usage()
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Get input filename from command line
    INPUT_FILE = sys.argv[1]
    
    # Validate input file
    is_valid, message = validate_input_file(INPUT_FILE)
    
    if not is_valid:
        print(f"Error: {message}")
        print()
        show_usage()
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Generate output filename based on input filename
    base_name = os.path.splitext(os.path.basename(INPUT_FILE))[0]
    OUTPUT_FILE = f'{base_name}_ping_results.csv'
    
    # Configuration
    MAX_WORKERS = 10  # Reduced for better stability on Windows
    
    print("Subdomain Ping Checker - Fixed Version")
    print("="*50)
    print(f"Input file: {INPUT_FILE}")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Platform: {platform.system()}")
    print(f"Current directory: {os.getcwd()}")
    print("="*50)
    
    # Load domains from file
    print(f"Loading domains from {INPUT_FILE}...")
    domains = load_domains_from_file(INPUT_FILE)
    
    if domains is None:
        print(f"\nError loading domains from '{INPUT_FILE}'")
        print("\nExpected file format:")
        print("https://example.com")
        print("https://subdomain.example.com") 
        print("http://another.example.com")
        print("subdomain.example.com")
        print("# This is a comment (optional)")
        print("\nPlease fix the file format and try again.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print(f"Found {len(domains)} domains to check")
    
    # Process domains
    results = []
    start_time = time.time()
    
    print("\nStarting ping checks...")
    print("This may take a while depending on the number of domains.")
    print("-" * 60)
    
    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all tasks
        future_to_domain = {
            executor.submit(process_single_domain, domain_url): domain_url 
            for domain_url in domains
        }
        
        # Process completed tasks
        completed = 0
        for future in as_completed(future_to_domain):
            domain_url = future_to_domain[future]
            try:
                domain, status, ip = future.result()
                results.append((domain, status, ip))
                
                completed += 1
                progress = (completed / len(domains)) * 100
                
                # Print progress and result
                status_color = "✓" if status == "ACTIVE" else "✗"
                print(f"[{completed:3}/{len(domains)}] ({progress:5.1f}%) {status_color} {domain:<40} -> {status}")
                
            except Exception as e:
                print(f"Error processing {domain_url}: {e}")
                results.append((extract_domain_from_url(domain_url), f'ERROR: {e}', 'Unknown'))
    
    # Sort results by status (Active first, then others)
    results.sort(key=lambda x: (x[1] != 'ACTIVE', x[0]))
    
    # Save results to CSV
    if save_results_to_csv(results, OUTPUT_FILE):
        print_summary(results)
        
        # Show some active examples
        active_domains = [r for r in results if r[1] == 'ACTIVE']
        if active_domains:
            print(f"\nFirst few active domains:")
            for domain, status, ip in active_domains[:5]:
                print(f"  ✓ {domain} -> {ip}")
    
    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")
    
    # Keep window open on Windows
    if platform.system().lower() == 'windows':
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
