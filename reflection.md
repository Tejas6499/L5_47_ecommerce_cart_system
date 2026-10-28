# Lab 5: Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the style issues from Flake8 and Pylint: unused imports and variables, the missing final newline, `== None`, long lines and the camelCase function names. Each one has a single obvious fix and does not change what the program does.

The hardest was the `eval` in `calculateDiscountedTotal`. Removing `eval` meant changing how the function is called, so I had to decide what the discount should look like instead (a percentage between 0 and 100) and update the caller in `main()`. While doing this I noticed the function ignored the quantity, which is a logic bug no tool reported. The `total_sales` global was also hard, because fixing the Pylint warning properly meant working out that the value was wrong in the first place and replacing it with a total calculated from the cart.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Bandit flagged MD5 as a high severity issue (B324). In this program the hash is only used to create an identifier for an item, not to protect a password or sign data, so the risk is small and this is close to a false positive. I still switched to SHA-256 because it costs nothing and removes the doubt.

The tools also missed things. None of them reported the live payment gateway key written in the code and printed to the terminal, and none of them noticed that the discounted total ignored the quantity or that `total_sales` was wrong. I only found these by reading the code and running it.

**3. How would you integrate static analysis tools into your actual software development workflow?**

I would run Flake8 and Pylint in the editor and as a pre-commit hook, so style problems are fixed before code is committed. In CI (for example GitHub Actions) I would run all three tools on every pull request, fail the build on any Bandit issue of medium or high severity, and fail if the Pylint score drops below an agreed minimum such as 9.5. Keeping the tool settings in a config file in the repository means everyone on the team gets the same results.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

The Pylint score went from 3.86/10 to 10.00/10, and Bandit and Flake8 now report no issues. The program can no longer run arbitrary code through `eval` or the shell, the secret key is no longer in the source or the output, and the checkout PIN comes from a secure random source. Removing an item that is not in the cart now returns `False` instead of hiding every error, and the audit log no longer leaks between calls. The output is also correct: the discounted total uses the quantity, the receipt is readable and shows a total, and the code is easier to follow with snake_case names and docstrings.
