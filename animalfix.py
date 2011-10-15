#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymclevel import mclevel
import wx
import random

def mkcoord(name, x,y,z):
	coord = mclevel.TAG_List()
	cx = mclevel.TAG_Double(name="", value=x)
	cy = mclevel.TAG_Double(name="", value=y)
	cz = mclevel.TAG_Double(name="", value=z)
	coord.insert(0, cx)
	coord.insert(1, cy)
	coord.insert(2, cz)
	coord.name = name
	return coord

def getsheepcol():
	r = random.randrange(0,10000)
	if r < 8184: # 81.84 % chance
		return 0 # White Wool
	elif r < 8684: # 5 % chance
		return 8 # Light Gray Wool
	elif r < 9184: # 5 % chance
		return 7 # Gray Wool
	elif r < 9684: # 5 % chance
		return 15 # Black Wool
	elif r < 9984: # 3 % chance
		return 12 # Brown Wool
	else: # 0.16 chance
		return 6 # Pink Wool

def mkanimal(name, x,y,z):
	if name == u"Chicken":
		animal = mclevel.Entity.Create(u"Chicken")
		animal["Health"] = mclevel.TAG_Short(name="Health", value=4)
	elif name == u"Pig":
		animal = mclevel.Entity.Create(u"Pig")
		animal["Health"] = mclevel.TAG_Short(name="Health", value=10)
		animal["Saddle"] = mclevel.TAG_Byte(name="Saddle", value=0)
	elif name == u"Cow":
		animal = mclevel.Entity.Create(u"Cow")
		animal["Health"] = mclevel.TAG_Short(name="Health", value=10)
	elif name == u"Sheep":
		animal = mclevel.Entity.Create(u"Sheep")
		animal["Health"] = mclevel.TAG_Short(name="Health", value=10)
		animal["Color"] = mclevel.TAG_Byte(name="Color", value=getsheepcol())
		animal["Sheared"] = mclevel.TAG_Byte(name="Sheared", value=0)
	elif name == u"Wolf":
		animal = mclevel.Entity.Create(u"Wolf")
		animal["Health"] = mclevel.TAG_Short(name="Health", value=8)
		animal["Owner"] = mclevel.TAG_String(name="Owner", value=u"")
		animal["Angry"] = mclevel.TAG_Byte(name="Angry", value=0)
		animal["Sitting"] = mclevel.TAG_Byte(name="Angry", value=0)
	else:
		raise ValueError("Unknown animlal type '{}'.".format(name))
	
	animal["Pos"] = mkcoord("Pos", x,y,z)
	animal["Motion"] = mkcoord("Motion", 0,0,0)
	animal["Rotation"] = mclevel.TAG_List(name="Rotation")
	animal["Rotation"].insert(0, mclevel.TAG_Float(name="", value=0))
	animal["Rotation"].insert(1, mclevel.TAG_Float(name="", value=0))
	animal["Fire"] = mclevel.TAG_Short(name="Fire", value=-1)
	animal["AttackTime"] = mclevel.TAG_Short(name="AttackTime", value=0)
	animal["HurtTime"] = mclevel.TAG_Short(name="HurtTime", value=0)
	animal["DeathTime"] = mclevel.TAG_Short(name="DeathTime", value=0)
	animal["Air"] = mclevel.TAG_Short(name="Air", value=300)
	animal["FallDistance"] = mclevel.TAG_Float(name="FallDistance", value=0)
	animal["OnGround"] = mclevel.TAG_Byte(name="OnGround", value=0)
	return animal

class AnimalFixFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="AnimalFix", size=(400, 600))
		
		self.mainpanel = wx.Panel(self, -1)
		vbox = wx.BoxSizer(wx.VERTICAL)
		
		vbox.Add(wx.StaticText(self.mainpanel,
label="""This tool will place animals into your Minecraft map, if you do not have any.
This sometimes happens to an old map after updating to >Beta 1.8.
PLEASE! Make a backup of your map before apply this tool on your map!""", style=wx.ALIGN_CENTER), 0, wx.EXPAND | wx.ALL, 5)
		
		vbox.AddStretchSpacer(1)
		
		hbox_mapin = wx.BoxSizer(wx.HORIZONTAL)
		hbox_mapin.Add(wx.StaticText(self.mainpanel, label="The directory of your old map:"), 0, wx.EXPAND | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
		self.map_input = wx.DirPickerCtrl(self.mainpanel)
		hbox_mapin.Add(self.map_input, 1, wx.EXPAND, 0)
		vbox.Add(hbox_mapin, 0, wx.EXPAND | wx.ALL, 5)
		
		vbox.AddStretchSpacer(1)
		
		self.process_txt   = wx.StaticText(self.mainpanel, label="")
		vbox.Add(self.process_txt, 0, wx.EXPAND | wx.ALL, 5)
		self.process_gauge = wx.Gauge(self.mainpanel, range=1000, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
		vbox.Add(self.process_gauge, 0, wx.EXPAND, wx.ALL, 5)
		
		vbox.AddStretchSpacer(1)
		
		self.letsgo = wx.Button(self.mainpanel, label="Lets do it!")
		vbox.Add(self.letsgo, 0, wx.EXPAND | wx.ALL, 5)
		
		self.mainpanel.SetSizer(vbox)
		vbox.Fit(self)
		self.SetMinSize(vbox.GetMinSize())
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.on_letsgo, id=self.letsgo.GetId())
	
	def on_letsgo(self, evt):
		try:
			world = mclevel.fromFile(self.map_input.GetPath())
		except ValueError:
			dialog = wx.MessageDialog(self, message="This is not a valid minecraft level!", caption="Could not load level", style=wx.OK | wx.ICON_ERROR)
			dialog.ShowModal()
			return True
		except IOError:
			dialog = wx.MessageDialog(self, message="Could not open directory!", caption="Could not load level", style=wx.OK | wx.ICON_ERROR)
			dialog.ShowModal()
			return True
		
		self.letsgo.Enable(False)
		
		overworld = world.getDimension(0)
		
		spawnon = [
			world.materials.Dirt.ID,
			world.materials.Grass.ID,
			world.materials.Gravel.ID,
			world.materials.Farmland.ID,
			world.materials.Snow.ID,
			world.materials.Ice.ID,
			world.materials.SnowLayer
		]
		
		treatasair = [
			world.materials.Air.ID,
			world.materials.TallGrass.ID,
			world.materials.Shrub.ID,
			world.materials.Flower.ID,
			world.materials.Rose.ID,
			world.materials.RedMushroom.ID,
			world.materials.BrownMushroom.ID,
		]
		
		animals = [u"Pig", u"Sheep", u"Chicken", u"Cow"]
		allanimals = animals + [u"Wolf"]
		
		# Count Chunks
		n_chunks = 0
		for _ in overworld.allChunks:
			n_chunks += 1
		
		i = 0
		nextanimalblock = random.randrange(1,11)
		for cx, cz in overworld.allChunks:
			i += 1
			chunk = overworld.getChunk(cx, cz)
			
			self.process_txt.SetLabel("{} / {}".format(i, n_chunks))
			self.process_gauge.SetValue(int((float(i) / float(n_chunks)) * 1000))
			self.Update()
			
			hasanimals = False
			for entity in chunk.Entities:
				if entity["id"].value in allanimals:
					hasanimals = True
					break
			if hasanimals:
				continue
			
			nextanimalblock -= 1
			if nextanimalblock > 0:
				continue
			
			nextanimalblock = random.randrange(1,11)
			
			countleaves = 0
			possible_spawnpoints = []
			for x in xrange(16):
				for y in xrange(16):
					noleaves = True
					for z in xrange(127, 0, -1):
						blkmat = chunk.Blocks[x,y,z]
						if blkmat not in treatasair:
							if (blkmat == world.materials.Leaves.ID) and noleaves:
								countleaves += 1
								noleaves = False
							else:
								if blkmat in spawnon:
									if world.materials.Leaves.ID not in chunk.Blocks[x,y,z+1:z+3]:
										# otherwise there would not be enough space...
										possible_spawnpoints.append((x,y,z+1))
								break
			
			isforest = countleaves >= (16*16*0.45) # We assume the chunk belongs to a forest, if there are 45% leaves seen from above.
			spawn_n = random.randrange(1,5)
			if spawn_n > len(possible_spawnpoints):
				spawn_n = len(possible_spawnpoints)
			if spawn_n == 0:
				continue
			else:
				random.shuffle(possible_spawnpoints)
				current_animals = allanimals if isforest else animals
				for x,z,y in possible_spawnpoints[0:spawn_n]:
					x = cx * 16 + x
					z = cz * 16 + z
					chunk.Entities.append(mkanimal(random.choice(current_animals), x,y,z))
				chunk.chunkChanged()
		
		self.process_txt.SetLabel("Saving data. This can take \"some\" time. Please be patient...")
		self.Update()
		
		world.generateLights();
		world.saveInPlace();
		
		dialog = wx.MessageDialog(self, message="Finished", caption="New animals were placed successfully.", style=wx.OK | wx.ICON_INFORMATION)
		dialog.ShowModal()
		
		self.process_gauge.SetValue(0)
		self.process_txt.SetLabel("")
		
		self.letsgo.Enable(True)
		return True

class AnimalFixApplication(wx.App):
	def OnInit(self):
		my_frame = AnimalFixFrame()
		my_frame.Show()
		self.SetTopWindow(my_frame)
		return True

if __name__ == '__main__':
	application = AnimalFixApplication()
	application.MainLoop()
