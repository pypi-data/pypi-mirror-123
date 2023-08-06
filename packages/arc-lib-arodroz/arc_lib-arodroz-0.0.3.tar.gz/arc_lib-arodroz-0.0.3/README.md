# strcpy
Python function allowing to copy a text in another one in a mutable way. That is regardless of whether the latter has enough space to accommodate the former.
## Usage
```python

    from arc_lib.text import strcpy

    text1 = "Hello"

    text2 = strcpy(text1, "world!", 6)
    
    print(text2)
```    
```console
    Hello world!
```    
```python
    text2 = strcpy(text1, "world!", 20)
    
    print(text2)
```    
```console
    Hello               world!
```    
```python
    text2 = strcpy(text1, "world!", 2)
    
    print(text2)
```    
```console
    Heworld!
```
## Installation
Install this through pip:
```shell
pip install arc_lib
```
