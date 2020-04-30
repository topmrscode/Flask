# convertir un object en dictionnaire --------------------------
# objectif : pour pouvoir l encode 
def convert_to_dict(obj):
  """
  A function takes in a custom object and returns a dictionary representation of the object.
  This dict representation includes meta data such as the object's module and class names.
  """
  obj_dict = {
  }
  obj_dict.update(obj.__dict__)
  return obj_dict