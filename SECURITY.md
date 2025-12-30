# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take the security of the Interval Arithmetic library seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do Not Open a Public Issue

Please **do not** open a public GitHub issue for security vulnerabilities, as this could put users at risk.

### 2. Report Privately

Send a detailed report to: **security@yourproject.com** (or use GitHub Security Advisories)

Include:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if any)
- Your contact information

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Assessment**: Within 1 week
- **Fix Timeline**: Depends on severity
  - Critical: Within 1-3 days
  - High: Within 1-2 weeks
  - Medium: Within 1 month
  - Low: Next regular release

### 4. Disclosure Process

1. We will investigate and validate the report
2. We will develop a fix
3. We will prepare a security advisory
4. We will release the fix
5. We will publicly disclose the vulnerability (with credit to reporter if desired)

## Security Best Practices

When using this library:

### Input Validation

The library includes built-in validation for:
- NaN values (rejected)
- Infinite values (rejected)
- Invalid interval constructions (rejected)

Example:
```python
from src.intervals import Interval
import math

# These will raise ValueError:
try:
    Interval(math.nan, 10)  # ValueError: Interval boundaries cannot be NaN
except ValueError:
    pass

try:
    Interval(math.inf, 10)  # ValueError: Interval boundaries cannot be infinite
except ValueError:
    pass
```

### Type Safety

Always use type hints and let your IDE/linter catch issues:

```python
from src.intervals import Interval

def process_interval(interval: Interval) -> float:
    return interval.measure()
```

### Error Handling

Always handle exceptions appropriately:

```python
from src.intervals import Interval, InvalidIntervalError

try:
    interval = Interval(10, 5)  # Invalid: start > end
except InvalidIntervalError as e:
    print(f"Invalid interval: {e}")
    # Handle error appropriately
```

### Dependency Security

We regularly update dependencies to address security issues. To ensure you have the latest secure versions:

```bash
pip install interval-arithmetic --upgrade
```

## Known Limitations

### Floating Point Precision

This library uses Python's `float` type, which is subject to floating-point precision issues. This is a fundamental limitation of floating-point arithmetic, not a security vulnerability.

Example:
```python
# This is expected behavior with floating-point arithmetic
0.1 + 0.2 == 0.3  # False (due to floating-point precision)
```

For applications requiring exact decimal arithmetic, consider using Python's `decimal.Decimal` type (not currently supported by this library).

### No Bounds on Interval Size

The library does not impose limits on interval sizes. Extremely large intervals may consume significant memory or cause performance issues.

Example:
```python
# This is allowed but may be impractical:
large_interval = Interval(-1e100, 1e100)
```

## Security Scanning

We use the following tools to maintain security:

- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability scanner
- **CodeQL**: Automated security analysis (GitHub)
- **Dependabot**: Automated dependency updates

## Acknowledgments

We appreciate security researchers who responsibly disclose vulnerabilities. If you report a valid security issue, we will:

1. Credit you in our security advisory (if you wish)
2. Thank you in our CHANGELOG
3. Consider you for our Hall of Fame

## Security Contacts

- **Email**: security@yourproject.com
- **GitHub Security Advisories**: https://github.com/yourusername/interval-arithmetic/security/advisories
- **PGP Key**: Available on request

## Version History

### Version 0.1.0

- ✅ Input validation for NaN and infinity
- ✅ Type safety with comprehensive type hints
- ✅ Clear error messages for invalid operations
- ✅ No known security vulnerabilities

---

Last updated: 2024-11-11