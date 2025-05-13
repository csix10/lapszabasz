class SortingByRectangles:
  def __init__(self, rectangles):
    self.rectangles = rectangles
    self.selection = {
      "latitude": self.latitude,
      "height": self.height,
      "area": self.area,
      "aspect_ratio" : self.aspect_ratio
    }

  #szélesség szerint sorrendbe rendezi téglalapok egy halmazát
  # - monotony=0: növekvő
  # - monotony=1 csökkenő
  def latitude(self, monotony):
    return sorted(self.rectangles, key=lambda x: x[0], reverse=monotony)

  #magasság szerint rendezi téglalapok egy halmazát
  def height(self, monotony):
    return sorted(self.rectangles, key=lambda x: x[1], reverse=monotony)

  #térület szerint sorrendbe rendezi téglalapok egy halmazát:
  def area(self, monotony):
    return sorted(self.rectangles, key=lambda x: x[0] * x[1], reverse=monotony)

  #Oldalrány szerint tendezi a téglalapok halzát
  def aspect_ratio(self, monotony):
    return sorted(self.rectangles, key=lambda x: min(x[0], x[1]) / max(x[0], x[1]), reverse=monotony)

  #SbS kevert javításánál használt rendezését hajtja végre
  def sort_c_aspect_ratio(self, algorithm, monotony, c):
    rectangles = self.selection[algorithm](monotony)
    rectangles_below_c = [rect for rect in rectangles if min(rect[0], rect[1]) / max(rect[0], rect[1]) < c]
    rectangles_above_c = [rect for rect in rectangles if min(rect[0], rect[1]) / max(rect[0], rect[1]) >= c]
    return  rectangles_above_c + rectangles_below_c

  #SbS maradék rendezés beállításai szerint rendez
  # - upload_site=1: a legkisebb területűre darabra helyezi le a szabandó téglalapot
  # - upload_site=2: a legelső táblára amire még ráfér helyezi le a téglalapot
  # - upload_site=21: a legelső táblán amire ráfér a legkisebb területű darabra helyezi le
  # - upload_site=3: a legkissebb szélességű darabra helyezi el a szabandó télalapot
  # - upload_site=0: nincs rendezés az üres darabok között
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

