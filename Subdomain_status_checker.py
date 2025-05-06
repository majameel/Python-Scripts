#!/usr/bin/env python3
import csv
import socket
import concurrent.futures
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
import sys
import time
import dns.resolver  # requires dnspython package

def check_subdomain(subdomain, timeout=15, use_get=True):
    """
    Check a subdomain for DNS resolution and HTTP/HTTPS response.
    Returns detailed information about the subdomain status.
    
    Parameters:
    - subdomain: The subdomain to check
    - timeout: Connection timeout in seconds
    - use_get: If True, tries GET request after HEAD fails
    """
    # Check DNS resolution (comprehensive)
    dns_status = "No"
    ip_addresses = []
    
    try:
        # Use dnspython for more comprehensive DNS checks
        answers = dns.resolver.resolve(subdomain, 'A')
        for rdata in answers:
            ip_addresses.append(str(rdata))
        
        if ip_addresses:
            dns_status = "; ".join(ip_addresses)
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, Exception) as e:
        # If any DNS resolution error occurs, return subdomain with no response
        return [subdomain, "No Response", dns_status, "N/A", "DNS Error"]
    
    # If we get here, DNS resolution succeeded
    
    # Check HTTP and HTTPS response with detailed error handling
    status_code = "No Response"
    response_time = "N/A"
    server_info = "Unknown"
    
    # Try HTTP first with HEAD
    try:
        start_time = time.time()
        http_response = requests.head(
            f"http://{subdomain}", 
            timeout=timeout, 
            allow_redirects=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        response_time = f"{(time.time() - start_time):.2f}s"
        status_code = str(http_response.status_code)
        
        # Get server information if available
        if 'Server' in http_response.headers:
            server_info = http_response.headers['Server']
    except (ConnectionError, Timeout, RequestException):
        # If HEAD fails and use_get is True, try GET for HTTP
        if use_get:
            try:
                start_time = time.time()
                http_response = requests.get(
                    f"http://{subdomain}", 
                    timeout=timeout,
                    allow_redirects=True,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    },
                    stream=True  # Don't download the whole content
                )
                # Just get headers and close connection
                http_response.close()
                response_time = f"{(time.time() - start_time):.2f}s"
                status_code = str(http_response.status_code)
                
                if 'Server' in http_response.headers:
                    server_info = http_response.headers['Server']
            except ConnectionError:
                status_code = "Connection Refused (HTTP)"
            except Timeout:
                status_code = "Timeout (HTTP)"
            except RequestException:
                # Try HTTPS
                try_https = True
        else:
            # Try HTTPS if HTTP fails
            try_https = True
    
    # Try HTTPS if HTTP failed
    if status_code == "No Response" or "Connection Refused" in status_code or "Timeout" in status_code:
        try:
            start_time = time.time()
            https_response = requests.head(
                f"https://{subdomain}", 
                timeout=timeout, 
                allow_redirects=True,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                verify=False  # Ignore SSL verification errors
            )
            response_time = f"{(time.time() - start_time):.2f}s"
            status_code = str(https_response.status_code)
            
            # Get server information if available
            if 'Server' in https_response.headers:
                server_info = https_response.headers['Server']
        except (ConnectionError, Timeout, RequestException):
            # If HEAD fails and use_get is True, try GET for HTTPS
            if use_get:
                try:
                    start_time = time.time()
                    https_response = requests.get(
                        f"https://{subdomain}", 
                        timeout=timeout,
                        allow_redirects=True,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        },
                        verify=False,  # Ignore SSL verification errors
                        stream=True  # Don't download the whole content
                    )
                    # Just get headers and close connection
                    https_response.close()
                    response_time = f"{(time.time() - start_time):.2f}s"
                    status_code = str(https_response.status_code)
                    
                    if 'Server' in https_response.headers:
                        server_info = https_response.headers['Server']
                except ConnectionError:
                    status_code = "Connection Refused (HTTPS)"
                except Timeout:
                    status_code = "Timeout (HTTPS)"
                except RequestException:
                    status_code = "No Response"
            else:
                status_code = "No Response"
    
    # Determine if this is likely a dangling DNS
    is_dangling = "Possible Dangling DNS" if (
        "No Response" in status_code or 
        "Connection Refused" in status_code or 
        "Timeout" in status_code
    ) else "Active"
    
    return [subdomain, status_code, dns_status, response_time, server_info, is_dangling]

def main():
    """
    Main function to process subdomain list and save results to CSV.
    Includes progress tracking and error handling.
    """
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Check if input file is provided
    if len(sys.argv) < 2:
        print("Usage: python check_subdomains.py subdomains.txt [max_workers] [timeout]")
        print("  max_workers: Optional parameter to set the number of concurrent threads (default: 20)")
        print("  timeout: Optional parameter to set the connection timeout in seconds (default: 15)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Get max workers from command line or default to 20
    max_workers = 20
    if len(sys.argv) >= 3:
        try:
            max_workers = int(sys.argv[2])
        except ValueError:
            print(f"Invalid max_workers value: {sys.argv[2]}. Using default: 20")
    
    # Get timeout from command line or default to 15 seconds
    timeout = 15
    if len(sys.argv) >= 4:
        try:
            timeout = int(sys.argv[3])
        except ValueError:
            print(f"Invalid timeout value: {sys.argv[3]}. Using default: 15 seconds")
    
    output_file = "subdomain_status.csv"
    
    # Read subdomains from file
    try:
        with open(input_file, 'r') as f:
            subdomains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    total = len(subdomains)
    print(f"Starting scan of {total} subdomains with {max_workers} concurrent workers and {timeout}s timeout...")
    
    # Create CSV file with headers
    try:
        with open(output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([
                'Subdomain', 
                'Status Code', 
                'DNS Resolution', 
                'Response Time', 
                'Server Info',
                'Status'
            ])
            
            # Process subdomains with progress tracking
            completed = 0
            start_time = time.time()
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_subdomain = {
                    executor.submit(check_subdomain, subdomain, timeout, True): subdomain for subdomain in subdomains
                }
                
                for future in concurrent.futures.as_completed(future_to_subdomain):
                    subdomain = future_to_subdomain[future]
                    
                    try:
                        result = future.result()
                        csv_writer.writerow(result)
                        
                        # Print dangling DNS candidates to console
                        if result[5] == "Possible Dangling DNS":
                            print(f"Possible dangling DNS: {subdomain} - {result[1]} - {result[2]}")
                    except Exception as e:
                        print(f"Error processing {subdomain}: {str(e)}")
                        csv_writer.writerow([subdomain, "Error", "Error", "N/A", str(e), "Error"])
                    
                    # Show progress
                    completed += 1
                    if completed % 5 == 0 or completed == total:
                        elapsed = time.time() - start_time
                        remaining = (elapsed / completed) * (total - completed) if completed > 0 else 0
                        print(f"Progress: {completed}/{total} subdomains checked " +
                              f"({(completed/total)*100:.1f}%) - " +
                              f"Elapsed: {elapsed:.1f}s, Est. remaining: {remaining:.1f}s")
    
        print(f"\nScan completed in {time.time() - start_time:.1f} seconds")
        print(f"Results saved to {output_file}")
        print("\nTo find potential dangling DNS records, look for entries with:")
        print("- Valid DNS Resolution (IP address)")
        print("- Status Code showing 'No Response', 'Connection Refused', or 'Timeout'")
        print("- Status column showing 'Possible Dangling DNS'")
    except PermissionError:
        print(f"Error: Permission denied when writing to '{output_file}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
