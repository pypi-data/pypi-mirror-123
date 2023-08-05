# `optimism`

A very small & simple unit-testing framework designed to provide all the
basic necessities to beginner programmers as simply as possible.

Designed by Peter Mawhorter.


## Dependencies

Works on Python versions 3.8 and up, with 3.9+ recommended.


## Installing

To install from PyPI, run the following command on the command-line:

```sh
python3 -m pip install optimism
```

Once it's installed, you can run the tests using:

```sh
TODO
```

## Usage

Use the `testCase` function to establish an expression as a test case.
Then use the `expectResult`, `expectOutputContains`, and/or
`expectCustom` functions to establish expectations for that test. Use
`provideInput` and/or `captureOutput` and related functions to deal with
input/output testing. Use `runFile` to create a test for an entire file.

See [the
documentation](https://cs.wellesley.edu/~pmwh/optimism/docs/optimism)
for more details on how to use it and what each function does.
