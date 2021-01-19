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
diff_month(date1: datetime, date2: datetime)
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
process_description(text: str, max_lenght: int) → str
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/utils.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_valid_url`

```python
is_valid_url(url: str) → bool
```






---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/utils.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `require_repo`

```python
require_repo(configuration: Dict) → bool
```

Returns true if a repo id is required for a project entry via `configuration.require_repo` or for compatibility reasons `configuration.require_github`. 



**Args:**
 
 - <b>`configuration`</b> (Dict):  The project configuration 



**Returns:**
 
 - <b>`bool`</b>:  if `configuration.require_repo` or `configuration.require_github` is True 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
