import re
import time

class PyWig:
  def __init__(self, htmlstring = None):
   htmlstring = ""
   self.htmlstring = htmlstring

  def create_page(self, title):
    self.htmlstring += f"<!DOCTYPE html>\n<html>\n<head>\n<title>{title}</title>\n</head>\n<body>"

  def add_header(self, header_type, text, style=None):
    headerlist = ["h1", "h2", "h3", "h4", "h5", "h6"]
    if header_type in headerlist:
      pass
    else:
      raise TypeError("Invalid header type.")
      return
    if style != None:
      self.htmlstring += f"\n<{header_type} style=\"{style}\">{text}</{header_type}>"
    else:
      self.htmlstring += f"\n<{header_type}>{text}</{header_type}>"

  def add_text(self, text, style=None):
    if style != None:
      self.htmlstring += f"\n<p style=\"{style}\">{text}</p>"
    else:
      self.htmlstring += f"\n<p>{text}</p>"

  def set_background_color(self, color):
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)
    if match:                      
      self.htmlstring = self.htmlstring.replace("<body>", f"<body style=\"background-color: {color}\">")
    else:
      raise ValueError("Invalid hex code.")
      return

  def add_link(self, text, link, style=None):
    if style != None:
      self.htmlstring += f"\n<a href=\"{link}\" style=\"{style}\">{text}</a>"
    else:
      self.htmlstring += f"\n<a href=\"{link}\">{text}</a>"

  def add_break(self):
    self.htmlstring += "<br>\n"

  def clear(self):
    self.htmlstring = ""

  def add_image(self, src, alt=None, style=None):
    if alt == None:
      alt = "An Image"
    if style != None:
      self.htmlstring += f"\n<img src=\"{src}\" alt=\"{alt}\" style=\"{style}\">"
    else:
      self.htmlstring += f"\n<img src=\"{src}\" alt=\"{alt}\">"

  def add_video(self, src):
    oggfile = src.replace(".mp4", ".ogg")
    self.htmlstring += f"\n<video controls>\n<source src=\"{src}\" type=\"video/mp4\">\n<source src=\"{oggfile}\" type=\"video/ogg\"\nVideo Not Supported\n</video>"

  def add_input(self, input_type, style=None):
    input_list = ["text", "password", "checkbox", "color", "date", "datetime-local",
    "email", "file", "hidden", "image", "month", "number", "radio", "range", "reset", 
    "submit", "search", "tel", "time", "url", "week"]
    if input_type in input_list:
      if style != None:
        self.htmlstring += f"\n<input type=\"{input_type}\" style=\"{style}\">"
      else:
        self.htmlstring += f"\n<input type=\"{input_type}\">"
    else:
      raise TypeError("Invalid Input Type")

  def auto_create(self, cooldown : int, max : int, filename : str):
    num = 0
    current = 0
    while current <= max:
      if num == 0:
        file = open(f"{filename}.html", "w")
        file.write(self.htmlstring)
        file.close()
      else:
        file = open(f"{filename}-{num}.html", "w")
        file.write(self.htmlstring)
        file.close()
      num += 1
      current += 1
      time.sleep(cooldown)

  def add_template(self, template, items):
    num = 0
    texts = items.split("|")
    try:
      while True:
        if f"item{num}" in template:
          template = template.replace(f"item{num}", texts[num])
          num += 1
        else:
          break
    except:
      raise ValueError("Error during template load. Make sure you have enough items to match your template.")
      return
    self.htmlstring += f"\n{template}"

  def save(self, pagename):
    self.htmlstring += "\n</body>\n</html>"
    file = open(f"{pagename}.html","w")
    file.write(self.htmlstring)
    file.close()
    self.htmlstring = self.htmlstring.replace("\n</body>\n</html>", "")