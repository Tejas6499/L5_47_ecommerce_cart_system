# Lab 5: Issues Found and Fixed

File: `ecommerce_cart_system.py`
Line numbers refer to the original file.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection | Security (Bandit B605, High) | 60 | `os.system("echo Receipt saved to: " + filename)` passes the file name to a shell, so a crafted file name could run any command. | Removed `os.system` and print the message with `print()`. No shell is started. |
| Weak hash function | Security (Bandit B324, High) | 49 | `hashlib.md5` is broken and should not be used for anything security related. | Replaced with `hashlib.sha256`. |
| Use of `eval` | Security (Bandit B307, Medium; Pylint W0123) | 42-45 | The discount was passed as a string and run with `eval`, so any Python code passed in would be executed. | The function now takes a numeric `discount_percent`, checks it is between 0 and 100 and calculates the price directly. |
| Hard-coded secret printed to output | Security (found manually, not flagged by any tool) | 72, 81 | A live payment gateway key was written in the source code and printed to the terminal. | The key is read from the `PAYMENT_GATEWAY_KEY` environment variable and the program only prints whether it is set. |
| Mutable default argument | Bug (Pylint W0102) | 15 | `audit_log=[]` is created once and shared by every call, so entries from earlier calls leak into later ones. | Default changed to `None`; the log is only written when a list is passed in. |
| Bare `except` with `pass` | Bug (Bandit B110, Low; Pylint W0702; Flake8 E722) | 26-29 | Every error was silently ignored, including ones that have nothing to do with a missing item. | Catch only `KeyError` and return `False`, return `True` on success. |
| Insecure random number for PIN | Security (Bandit B311, Low) | 53 | `random.randint` is predictable and not suitable for a checkout PIN. | Replaced with `secrets.randbelow`. |
| Wrong and unused sales total | Bug (Pylint W0603, C0103; found manually) | 12, 16, 20 | `total_sales` ignored the items already in the cart, was not reduced when an item was removed, and was never used. | Removed the global variable. Added `calculate_cart_total()`, which works out the total from the cart itself. |
| Discount ignores quantity | Bug (found manually by running the program) | 42-45, 76 | `calculateDiscountedTotal` returned the discounted price of one unit (22.5) even though the cart has 2 of ITEM1. | The function now uses price x quantity, giving 45.0 for ITEM1 at 10% off. |
| Price truncated in audit log | Bug (Pylint C0209; found manually) | 21 | `%d` cuts off the decimal part of the price. | Changed to an f-string with `:.2f`. |
| File not closed safely, no encoding | Quality (Pylint R1732, W1514) | 57-59 | The file is not closed if `write` fails, and the encoding depends on the system. | Used `with open(filename, "w", encoding="utf-8")`. |
| Receipt is a raw dictionary | Quality (found manually) | 58 | The receipt file contained `str(cart_items)`, which is not readable. | The receipt now has one line per item and a total. |
| Unused imports and variables | Quality (Pylint W0611, W0612; Flake8 F401, F841) | 4, 33, 43, 65 | `math`, `handling_fee`, `base_price` and `k` were never used. | Removed them. |
| Parameter shadows global | Quality (Pylint W0621) | 63 | `getCartSummary(cart_items)` hides the global `cart_items`. | Renamed the parameter to `items`. |
| Comparison to `None` and redundant `if` | Style (Pylint C0121, R1703, R1705; Flake8 E711) | 34-39 | `== None` and an `if/else` that only returns `True`/`False`. | `return item is not None and item["qty"] > 0`. |
| Naming and missing docstrings | Style (Pylint C0103, C0114, C0116) | 1, 15-71 | Functions used camelCase and there were no docstrings. | Renamed to snake_case and added module and function docstrings. |
| Code runs on import | Quality (found manually) | 84 | `main()` ran whenever the file was imported. | Added `if __name__ == "__main__":`. |
| Line length and final newline | Style (Flake8 E501, W292; Pylint C0304) | 76, 84 | One line was longer than 79 characters and the file had no final newline. | Wrapped the long lines and added a final newline. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 3.86/10 | 10.00/10 |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | No issues |
| Flake8 | 7 issues | No issues |
