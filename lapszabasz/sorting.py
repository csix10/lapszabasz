class SortingByRectangles:
  def __init__(self, rectangles):
    self.rectangles = rectangles
    self.selection = {
      "latitude": self.latitude,
      "height": self.height,
      "area": self.area,
      "aspect_ratio" : self.aspect_ratio
    }

  #szelesseg szerint sorrendbe rendezi teglalapok egy halmazat
  # - monotony=0: novekvo
  # - monotony=1 csokkeno
  def latitude(self, monotony):
    return sorted(self.rectangles, key=lambda x: x[0], reverse=monotony)

  #magassag szerint rendezi teglalapok egy halmazat
  def height(self, monotony):
    return sorted(self.rectangles, key=lambda x: x[1], reverse=monotony)

  #terulet szerint sorrendbe rendezi teglalapok egy halmazat:
  def area(self, monotony):
    return sorted(self.rectangles, key=lambda x: x[0] * x[1], reverse=monotony)

  #Oldalrany szerint tendezi a teglalapok halzat
  def aspect_ratio(self, monotony):
    return sorted(self.rectangles, key=lambda x: min(x[0], x[1]) / max(x[0], x[1]), reverse=monotony)

  #SbS kevert javitasanal hasznalt rendezeset hajtja vegre
  def sort_c_aspect_ratio(self, algorithm, monotony, c):
    rectangles = self.selection[algorithm](monotony)
    rectangles_below_c = [rect for rect in rectangles if min(rect[0], rect[1]) / max(rect[0], rect[1]) < c]
    rectangles_above_c = [rect for rect in rectangles if min(rect[0], rect[1]) / max(rect[0], rect[1]) >= c]
    return  rectangles_above_c + rectangles_below_c

  #SbS maradek rendezes beallitasai szerint rendez
  # - upload_site=1: a legkisebb teruleture darabra helyezi le a szabando teglalapot
  # - upload_site=2: a legelso tablara amire meg rafer helyezi le a teglalapot
  # - upload_site=21: a legelso tablan amire rafer a legkisebb teruletu darabra helyezi le
  # - upload_site=3: a legkissebb szelessegu darabra helyezi el a szabando telalapot
  # - upload_site=0: nincs rendezes az ures darabok kozott
  def step_setting(self, sizes, upload_site):
    if upload_site==1:
        sizes = sorted(sizes, key=lambda x: x[0] * x[1], reverse=0)
    elif upload_site==2:
        sizes = sorted(sizes, key=lambda x: x[3])
    elif upload_site==21:
        sizes = sorted(sizes, key=lambda x: x[0] * x[1], reverse=0)
        sizes = sorted(sizes, key=lambda x: x[3])
    elif upload_site==3:
        sizes = sorted(sizes, key=lambda x: x[0], reverse=0)
    return sizes

