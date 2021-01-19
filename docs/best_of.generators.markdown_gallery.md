<!-- markdownlint-disable -->

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_gallery.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `best_of.generators.markdown_gallery`
Gallery view for a best-of list. 

For each project, it shows an image (or takes a screenshot of the homepage) and some information. Note that only a selected subset of project information is shown (compared to MarkdownListGenerator). See the example at: https://github.com/jrieke/best-of-streamlit 

Gallery view allows for some additional configuration args, see README.md. 

**Global Variables**
---------------
- **DUMMY_IMAGE**

---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_gallery.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `chunker`

```python
chunker(seq: list, size: int) → Generator
```

Iterates over a sequence in chunks. 


---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_gallery.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `shorten`

```python
shorten(s: str, max_len: int) → str
```

Shorten a string by appending ... if it's too long. 


---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_gallery.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `save_screenshot`

```python
save_screenshot(
    url: str,
    img_path: str,
    sleep: int = 5,
    width: int = 1024,
    height: int = 576
) → None
```

Loads url in headless browser and saves screenshot to file (.jpg or .png). 


---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_gallery.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_project_html`

```python
generate_project_html(
    project: Dict,
    configuration: Dict,
    labels: Dict = None
) → str
```

Generates the content of a table cell for a project. 


---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_gallery.py#L146"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_table_html`

```python
generate_table_html(projects: list, config: Dict, labels: Dict) → str
```

Generates a table containing several projects. 


---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_gallery.py#L163"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_category_gallery_md`

```python
generate_category_gallery_md(
    category: Dict,
    config: Dict,
    labels: list,
    title_md_prefix: str = '##'
) → str
```

Generates markdown gallery for a category, containing tables with projects. 


---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_gallery.py#L224"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_short_toc`

```python
generate_short_toc(categories: OrderedDict, config: Dict) → str
```

Generate a short TOC, which is just all category names in one line. 


---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_gallery.py#L254"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_md`

```python
generate_md(categories: OrderedDict, config: Dict, labels: list) → str
```

Generate the markdown text. 

This is a near-complete copy of the same method in markdown_list but it uses the functions in this file. 


---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_gallery.py#L334"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MarkdownGalleryGenerator`





---

#### <kbd>property</kbd> name







---

<a href="https://github.com/best-of-lists/best-of-generator/blob/main/src/best_of/generators/markdown_gallery.py#L339"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_output`

```python
write_output(
    categories: OrderedDict,
    projects: List[Dict],
    config: Dict,
    labels: list
) → None
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
