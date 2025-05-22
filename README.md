# Python Scripts Collection 🐍

A collection of Python tools for domain and subdomain analysis, status checking, and network testing.

## 📋 Available Scripts

### 1. [Subdomain Status Checker](./subdomain_status.md) 🌐
**File:** `Subdomain_status_checker.py`

A Python tool for identifying active subdomains and detecting dangling DNS records.

**Features:**
- Tests both HTTP and HTTPS connections with HEAD and GET fallbacks
- Advanced DNS resolution with dnspython
- Concurrent processing for fast scanning
- Real-time progress tracking with ETA
- CSV output with status codes, DNS info, and response times
- Automatic detection of potential dangling DNS records

**Quick Usage:**
```bash
python Subdomain_status_checker.py domains.txt
```

---

### 2. [Subdomain Ping Checker](./docs/subdomain-ping-checker.md) 🏓
**File:** `Ping_test_on_multiple_websites.py`

A multi-threaded ping utility that tests domain availability and resolves IP addresses.

**Features:**
- Multi-threaded pinging for fast results
- Cross-platform support (Windows, Linux, macOS)
- DNS resolution to get IP addresses
- CSV export with detailed results
- Progress tracking with real-time updates
- Wildcard domain filtering

**Quick Usage:**
```bash
python Ping_test_on_multiple_websites.py domains.txt
```

---

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/majameel/Python-Scripts.git
   cd Python-Scripts
   ```

2. **Choose your tool:**
   - For comprehensive subdomain analysis → Use **Subdomain Status Checker**
   - For simple ping tests → Use **Subdomain Ping Checker**

3. **Prepare your input file:**
   ```
   https://example.com
   https://subdomain.example.com
   domain.com
   ```

4. **Run the script:**
   ```bash
   python <script_name> <input_file>
   ```

## 📊 Comparison

| Feature | Status Checker | Ping Checker |
|---------|----------------|--------------|
| **HTTP/HTTPS Testing** | ✅ Advanced | ❌ No |
| **Ping Testing** | ❌ No | ✅ Yes |
| **DNS Resolution** | ✅ Advanced | ✅ Basic |
| **Dangling DNS Detection** | ✅ Yes | ❌ No |
| **Response Time** | ✅ Yes | ✅ Yes |
| **Status Codes** | ✅ Yes | ❌ No |
| **Concurrent Processing** | ✅ Yes | ✅ Yes |
| **Cross-Platform** | ✅ Yes | ✅ Yes |

## 🎯 When to Use Which Tool

### Use **Subdomain Status Checker** when:
- You need comprehensive web service analysis
- You want to detect dangling DNS records
- You need HTTP status codes and response details
- You're doing security assessments
- You want to check SSL/TLS connectivity

### Use **Subdomain Ping Checker** when:
- You need simple network connectivity tests
- You want to check if hosts are reachable via ICMP
- You're doing basic network troubleshooting
- You need IP address resolution
- You want lightweight, dependency-free checking

## 📁 Repository Structure

```
Python-Scripts/
├── README.md                          # This file
├── Subdomain_status_checker.py        # Advanced HTTP/HTTPS checker
├── Ping_test_on_multiple_websites.py  # Simple ping checker
├── docs/
│   ├── subdomain-status-checker.md    # Detailed documentation
│   └── subdomain-ping-checker.md      # Detailed documentation
└── examples/
    ├── sample_domains.txt              # Example input file
    └── sample_results.csv              # Example output
```

## 🛠️ Requirements

- **Python 3.6+**
- **No additional packages** for Ping Checker
- **dnspython** for Status Checker: `pip install dnspython`

## 📖 Documentation

- [Subdomain Status Checker - Full Documentation](./docs/subdomain-status-checker.md)
- [Subdomain Ping Checker - Full Documentation](./docs/subdomain-ping-checker.md)

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Happy domain checking!** 🎉


###

###
