from PIL import Image, ImageTk, ImageDraw
class TitleButtons:
	__image = None

	def __init__(self, image, size):
		self.__image = Image.open(image)
		self.__image = self.__image.resize(size)

	def makePhoto(self):
		return ImageTk.PhotoImage(self.__image)