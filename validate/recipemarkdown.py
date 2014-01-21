import markdown
from bs4 import BeautifulSoup

def parse_list(parent, base_url):
  res = []
  for node in parent.children:
    if node.name == 'li':
      obj = {}
      obj['text'] = node.text
      for i in node.children:
        if i.name == 'img':
          obj['img'] = base_url + i.get('src')
      res.append(obj)
  return res

def parse_recipe_markdown(md, obj, base_url):
  html = markdown.markdown(md)
  soup = BeautifulSoup(html)
  if soup.img:
    obj['img'] = base_url + soup.img.get('src')
  parsing = 'title'
  if soup.h1 and soup.h1.string:
    obj['title'] = soup.h1.string
    node = soup.h1.nextSibling
    parsing = 'summary'
    obj[parsing] = []
    while node:
      if node.name == 'h2':
        parsing = node.text.lower()
        obj[parsing] = []
      else:
        if node.name == 'p':
          if node.text and node.text != '':
            obj[parsing].append(node.text)
        elif node.name == 'ul':
          obj[parsing] = parse_list(node, base_url)
        elif node.name == 'ol':
          obj[parsing] = parse_list(node, base_url)
      node = node.nextSibling
  if not obj.has_key('ingredients') or not obj.has_key('steps') or not obj.has_key('title'):
    obj['error'] = 'Some required sections missing - must have title, ingredients, steps'

  return obj


if __name__ == '__main__':
  doc = """
Super simple guacamole
======================
![Super simple guacamole](imgs-super-simple-guacamole/main.jpg "Super simple guacamole")


Some guacamole recipes call for many ingredients and can be a pain to prepare.  This super simple guac can be thrown together in a couple of minutes and tastes great.

Ingredients
-----------
- 2 ripe avocados
- 1 lime
- 2 tbsp cilantro

Steps
-----
1. Use a spoon to scoop the flesh of the avocados into a bowl.
2. Mash with a fork until fairly smooth and creamy.  Preserve some small solid chunks to add texture.
3. Add the juice of the lime.
![juicing the lime](imgs-super-simple-guacamole/step-3-lime.jpg "Juicing the lime")
4. Add the cilantro.
5. Mix thoroughly.

Serving
-------
Great with tortilla chips, in tacos and burritos.
"""
  print parse_recipe_markdown(doc, {'name': 'super-simple-guacamole'}, 'http://www/')