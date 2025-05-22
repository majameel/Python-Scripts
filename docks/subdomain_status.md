# Subdomain Status Checker

A Python tool for identifying active subdomains and detecting dangling DNS records.

## Features

- Tests both HTTP and HTTPS connections with HEAD and GET fallbacks
- Advanced DNS resolution with dnspython
- Concurrent processing for fast scanning
- Real-time progress tracking with ETA
- CSV output with status codes, DNS info, and response times
- Automatic detection of potential dangling DNS records

## Installation

```bash
# Clone repository
git clone https://github.com/your-username/subdomain-status-checker.git
cd subdomain-status-checker

# Install dependencies
pip install requests dnspython urllib3

```
## Usage
```
# Basic usage
python check_subdomains.py subdomains.txt

# With custom workers and timeout
python check_subdomains.py subdomains.txt 25 30

Parameters:

subdomains.txt: File with subdomains (one per line)

max_workers (optional): Concurrent threads (default: 20)

timeout (optional): Connection timeout in seconds (default: 15)

```
## Output
The script generates subdomain_status.csv with columns:

Subdomain
Status Code
DNS Resolution (IP addresses)
Response Time
Server Info
Status (Active/Possible Dangling DNS)

Dangling DNS records are identified when a subdomain resolves to an IP but doesn't respond to web requests

## Security Notes
Dangling DNS records may present security risks including subdomain takeover vulnerabilities, phishing opportunities, and unauthorized access vectors.
