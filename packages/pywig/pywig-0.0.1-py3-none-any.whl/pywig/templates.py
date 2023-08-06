templates = {
    "standard": "<h1>item0</h1>\n<p>item1</p>",
    "links": "<h1>item0</h1>\n<p>item1</p>\n<a href=\"item2\">item3</a>"
}
def load_template(template):
    if template in templates:
      file = templates[template]
      return file
    else:
      raise TypeError("Invalid template.")