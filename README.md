# wordle-solutions

API that provides Wordle (ES) solutions.

## Usage

```bash
curl https://wordle-solutions.herokuapp.com/<date-iso-format>
```

Examples:
```bash
curl https://wordle-solutions.herokuapp.com/ # Returns all solutions
```

```bash
curl https://wordle-solutions.herokuapp.com/2022-02-06 # Returns solution of the day
```

Recommendation: use jq to parse.

![Output example](img/output-example.png)

## Future work (not me)
Maybe a front-end?

## Disclaimer
Crappy code.
