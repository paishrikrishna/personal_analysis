import keen


class keen_dashboard_queries:
  keen.project_id = "631385288508994183df0c50"
  keen.write_key = "74290c472aae014c5512b212da8886303e31221a847b286cfc279ba28d416f7912244e60e952dad15221d6c4bcfc25e41081d78a9fd8c35a30934b32f864e158c90993be58041d99beed85b55ed293872fda46246da0dc6f138a081626ae7301"
  
  def __init__(self):
    self.keen = keen
    
  def push_data(self,stream_name):
    try:
      self.keen.add_event(stream_name,{"Test":'Test'})
      return 200
    except:
      return 400


