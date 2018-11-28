import player
import random
import graphicsFunc
import logic
import copy
random.seed(11)
class PlayerR(player.Player):

	def __init__(self):
		super().__init__("Right")

	def initialHand(self, data):
		data.heightRight = data.height / 2 - 15
		data.altMultR = 1
		for i in range(1,14):
			self.addTile(data)
		self.reorganizeTiles(data)

	# returns the sequential hand order to check for melds after the current player
	def handOrder(self, data):
		return [data.T, data.L, data.B]

	# recenters tiles based on the number of tiles left in the hand
	def reorganizeTiles(self, data):
		newTiles = []
		data.heightRight = data.height / 2 - 15
		tilesInd = 0
		for i in range(1, len(self.tiles) + 1):
			newTiles.append([8.5 * data.width / 10, data.heightRight, self.tiles[tilesInd][2], False])
			data.heightRight += 40 * data.altMultR * i
			data.altMultR *= -1
			tilesInd += 1
		self.tiles = newTiles

	# draws a tile from the available tiles
	def addTile(self, data):
		randInd = random.randint(0, len(data.drawPile) - 1)
		drawnTile = data.drawPile.pop(randInd)
		# draw another tile for flowers and seasons
		if drawnTile[1][0] == "s" or drawnTile[1][0] == "f":
			self.melds.append([None, None, drawnTile, False])
			self.addTile(data)
			return
		# add new tile at corresponding position
		self.tiles.append([8.5 * data.width / 10, data.heightRight, drawnTile, False])
		self.tileNames.append(drawnTile[1])
		# change position of next tile
		i = len( self.tiles)
		data.heightRight += 40 * data.altMultR * i
		data.altMultR *= -1

	# draws horizontal tile with hidden image
	def drawTiles(self, canvas, data):
		for piece in self.tiles:
			pX = piece[0]
			pY = piece[1]
			self.threeDTile(canvas, pX, pY)
			# in no cpu version, do not show tiles
			if data.cpus != []:
				img = data.backHPng
			else:
				img = piece[2][0]
			canvas.create_image(pX, pY, image=img)

	# creates 3d appearing mahjong piece horizontally
	def threeDTile(self, canvas, pX, pY):
		canvas.create_rectangle(pX - 23, pY - 11, pX + 17, pY + 18,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 22, pY - 12, pX + 18, pY + 17,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 21, pY - 13, pX + 19, pY + 16,  fill ="white", width = 0)
		canvas.create_rectangle(pX - 20, pY - 14, pX + 20, pY + 15,  fill ="white", width = 0)

	# draws all the melds at bottom
	def drawMelds(self, canvas, data):
		i = 0
		for piece in self.melds:
			pX = data.width - 35
			pY = 90 + 55 * i
			graphicsFunc.threeDTile(canvas, pX, pY)
			canvas.create_image(pX, pY, image=piece[2][0])
			i += 1
