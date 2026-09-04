# fertility.py audit

## Scope

This document reconstructs the behavior of the supplied fertility benchmark from the original source and aligns it to the reported output.

## Source inspected

- original/starter_kit/fertility.py
- submission/data/raw/starter_kit/fertility.py

## Implementation summary

### 1. Input

The program accepts one or more `--corpus` arguments in the format:

`LANG=PATH`

It also accepts a tokenizer selector via `--tokenizer` and defaults to `gpt2`.

The code path for the default implementation is:

```python
enc = tiktoken.get_encoding(spec)
return enc.encode
```

This means the benchmark is using the `gpt2` tokenizer encoding from `tiktoken` and tokenizes each line by calling `enc.encode(line)`.

### 2. Preprocessing

Before tokenization:

```python
line = raw.strip()
if not line:
    continue
line = unicodedata.normalize("NFC", line)
```

This removes leading and trailing whitespace and normalizes the text to Unicode NFC before analysis.

### 3. Core metric definition

For each line:

```python
line = line.lower()
tokens = encode(line)
words = line.split(" ")
chars = len(line)
per_line_fertility.append(len(tokens) / len(words))
per_line_tpc.append(len(tokens) / chars)
```

This yields:

- fertility per line: `len(tokens) / len(words)`
- tok/char per line: `len(tokens) / len(line)`

Then the overall result is:

```python
n = len(per_line_fertility)
return sum(per_line_fertility) / n, sum(per_line_tpc) / n
```

So the metric is the arithmetic mean over line-level ratios, not the corpus-level ratio:

$$
F = \frac{1}{N}\sum_{i=1}^{N} \frac{T_i}{W_i}
$$

and

$$
C = \frac{1}{N}\sum_{i=1}^{N} \frac{T_i}{L_i}
$$

where:

- $T_i$ = token count for line $i$
- $W_i$ = number of words in line $i$ using `line.split(" ")`
- $L_i$ = character count of the lowercased line after NFC normalization and strip

### 4. Word counting details

Words are counted using:

```python
words = line.split(" ")
```

This has three important effects:

1. It counts empty strings caused by repeated spaces, leading spaces, or trailing spaces.
2. It does not split on tabs or other whitespace characters.
3. It treats punctuation as part of the token, and word count is based only on space separators.

Therefore the implementation is not a general-purpose whitespace-agnostic word counter; it is a space-delimited approximation.

### 5. Token counting details

The program does not add BOS/EOS or any special tokens beyond the tokenizer's default behavior for `tiktoken` `gpt2` encoding. For the default path, `enc.encode(s)` returns the raw token ids produced by the GPT-2 encoder with no extra sentinel tokens.

### 6. Aggregation behavior

The implementation computes the mean of per-line ratios. This is not equivalent to the corpus-level ratio:

$$
\frac{\sum_i T_i}{\sum_i W_i}
$$

unless all lines have identical word counts and/or tokenization scales are uniform across lines.

### 7. Output behavior

The script prints a table with columns:

- `lang`
- `fertility (tok/word)`
- `tok/char`

Then, for multiple languages, it prints a ratio relative to the first language in the input list:

```python
ratio = results[lang][0] / results[base][0]
```

This is a mean-ratio comparison between the selected language and the first corpus listed.

## Direct conclusion from the implementation

The supplied implementation measures the arithmetic mean of per-line token-to-word and token-to-character ratios, using a GPT-2 tokenizer on lowercased, NFC-normalized, stripped lines, and a space-split word count.

This is a valid baseline for reproduction, but it is not equivalent to a general-purpose cross-language fertility measure unless the corpus and preprocessing are carefully controlled.
