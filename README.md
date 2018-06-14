# blacklist-pre-commit-hook

A pre-commit hook for blacklisting certain functions.

The `blacklist` hook will check for function calls to functions that are big no-nos, like `eval`, and will issue
a warning if it finds any. By default, it will only check for `eval`, but you can customize the blacklisted name list by
passing the `--blacklisted-names` argument on the command line.

## Installation

To install, just add the hook to your `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/skorokithakis/blacklist-pre-commit-hook
    rev: master
    hooks:
    - id: blacklist
      args: ["--blacklisted-names=eval,print,int"]
```

That should be all!
