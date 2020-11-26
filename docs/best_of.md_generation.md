<!-- markdownlint-disable -->

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `best_of.md_generation`





---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_metrics_info`

```python
generate_metrics_info(project: Dict, configuration: Dict) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_label_info`

```python
get_label_info(label: str, labels: list) → Dict
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L103"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_project_labels`

```python
generate_project_labels(project: Dict, labels: list) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L142"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_license_info`

```python
generate_license_info(project: Dict, configuration: Dict) → Tuple[str, int]
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L173"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_links_list`

```python
generate_links_list(project: Dict, configuration: Dict) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L198"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_pypi_details`

```python
generate_pypi_details(project: Dict, configuration: Dict) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L261"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_conda_details`

```python
generate_conda_details(project: Dict, configuration: Dict) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L316"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_maven_details`

```python
generate_maven_details(project: Dict, configuration: Dict) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L363"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_dockerhub_details`

```python
generate_dockerhub_details(project: Dict, configuration: Dict) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L421"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_npm_details`

```python
generate_npm_details(project: Dict, configuration: Dict) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L485"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_github_details`

```python
generate_github_details(project: Dict, configuration: Dict) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L586"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_project_body`

```python
generate_project_body(project: Dict, configuration: Dict) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L615"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_project_md`

```python
generate_project_md(project: Dict, configuration: Dict, labels: list) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L658"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_category_md`

```python
generate_category_md(
    category: Dict,
    configuration: Dict,
    labels: list,
    title_md_prefix: str = '##'
) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L692"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_legend`

```python
generate_legend(configuration: Dict, title_md_prefix: str = '##') → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L725"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `process_md_link`

```python
process_md_link(text: str) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L730"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_toc`

```python
generate_toc(categories: OrderedDict) → str
```






---

<a href="https://github.com/ml-tooling/best-of-generator/blob/main/src/best_of/md_generation.py#L755"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_md`

```python
generate_md(categories: OrderedDict, configuration: Dict, labels: list) → str
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
