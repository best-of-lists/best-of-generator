<!-- markdownlint-disable -->

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `best_of.utils`




**Global Variables**
---------------
- **url_validator**

---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/utils.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `simplify_str`

```python
simplify_str(text: str) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/utils.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `diff_month`

```python
diff_month(date1: datetime, date2: datetime) → int
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/utils.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `clean_whitespaces`

```python
clean_whitespaces(text: str) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/utils.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `simplify_number`

```python
simplify_number(num: int) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/utils.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `remove_special_chars`

```python
remove_special_chars(text: str) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/utils.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `process_description`

```python
process_description(text: str, max_length: int) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/utils.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_valid_url`

```python
is_valid_url(url: str) → bool
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/utils.py#L74"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `exit_process`

```python
exit_process(code: int = 0) → None
```

Exit the process with exit code. 

`sys.exit` seems to be a bit unreliable, process just sleeps and does not exit. So we are using os._exit instead and doing some manual cleanup. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
