import os
from recipemarkdown import parse_recipe_markdown

def test_validate_recipes():
  for filename in os.listdir('..'):
    if filename.startswith('recipe'):
      rf = file('..' + os.sep + filename, 'r')
      data = ''.join(rf.readlines())
      res = parse_recipe_markdown(data, {}, 'http://test/')
      if res.has_key('error'):
        print 'Error: %s %s' % (filename, res['error'])
      assert not res.has_key('error')
