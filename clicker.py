import tkinter as tk
from idlelib.tooltip import Hovertip as tip

class Gear:
	def __init__(self, name, description, tip, cost, quantity=0, per_second=0, limit=0,
					multiplier=None, synergy_unlocked=None, synergy_building=None):
		self.name = name
		self.description = description
		self.tip = tip
		self.cost = cost
		self.quantity = quantity
		self.per_second = per_second
		self.limit = limit
		self.multiplier = multiplier
		self.synergy_unlocked = synergy_unlocked
		self.synergy_building = synergy_building
class Clicker:
	def __init__(self, parent):
		self.parent = parent
		self.tooltips = {}
		self.the_button = tk.Button(parent, text='Click the button', width=20, height=5, command=self.increment)	
		self.current_clicks = 0
		self.gear = {}
		self.gear['clicker'] = Gear('clicker', 'Clicks per click: (%d): 1',
			'Click again whenever you click.', 10, quantity=1, limit=100)
		self.gear['click booster'] = Gear('click booster',
			'Multiplicative click booster: (%d) : 0)', 'Doubles your clicks.', 50, limit=5)
		self.gear['noob training'] = Gear('noob training', 'Double noobs\' clicking: (%d): 0',
			'"See, here\'s how you click things."', 50, limit=5)
		self.gear['orcish pride'] = Gear('orcish pride', 'Goblins get braver with their gremlin brethren: (%d)',
			'Adds to your goblins\' clicks per second for every gremlin you have.', 1000, limit=1)
		self.gear['noob clicker'] = Gear('noob clicker', 'Noob clicker: (%d): 0',
			'A noob at clicking, but they care!', 15, multiplier=self.gear['noob training'], per_second=1)
		self.gear['gremlin'] = Gear('gremlin', 'A gremlin to click things: (%d): 0',
			'Gremlins enjoy clicking. Really.', 50, per_second=5)
		self.gear['goblin'] = Gear('goblin', 'A goblin to provide you with clicks: (%d): 0',
			'Goblins click more than gremlins.', 200, per_second=30,
			synergy_unlocked=self.gear['orcish pride'], synergy_building=self.gear['gremlin'])
		self.gear['inclined plane'] = Gear('inclined plane','Roll some clicks your way: (%d): 0',
			'Observe clicks in slow motion.', 500, per_second=125)
		self.gear['pulley'] = Gear('pulley', 'Pull some clicks to you: (%d): 0',
			'Not frictionless.', 2000, per_second=750)
		self.gear['lever'] = Gear('lever', 'Pry some clicks up: (%d): 0',
			'Archimedes would be proud.', 10000, per_second=5000)
		self.gear['wedge'] = Gear('wedge', 'Stuff some extra clicks in there: (%d): 0',
			'Can I axe you a question?', 100000, per_second=75000)
		self.gear['elbow grease'] = Gear('elbow grease', 'Click the old fashioned way: (%d): 0',
			'Surprisingly easy.', 500000, per_second=500000)

		for gear in (self.gear.values()):
			gear.button = tk.Button(parent,text=gear.description % self.gear[gear.name].cost, command=lambda x=gear: self.purchase(x))
																	#x=gear to define when defined, instead of defined when called	
			gear.tooltip = tip(gear.button, gear.tip + ' - (%d/s)' % gear.per_second)
		
		self.current_click_label = tk.Label(parent, text='0')
		self.the_button.grid(row=0, column=0)
		self.current_click_label.grid(row=0, column=1)
		self.per_second_label = tk.Label(parent, text='0')
		self.per_second_label.grid(row=0, column=2)
		manual_row = 0
		auto_row = 0
		for name in sorted(self.gear, key=lambda x: self.gear[x].cost):
			if self.gear[name].per_second:
				manual_row += 1
				row = manual_row
				column = 2
			else:
				auto_row += 1
				row = auto_row
				column = 1
			self.gear[name].button.grid(row=row, column=column)
		
		self.update()
	
	def increment(self):
		self.current_clicks += self.gear['clicker'].quantity * 2**self.gear['click booster'].quantity
		self.current_click_label.config(text='{:,}'.format(self.current_clicks))

	def purchase(self, gear):
		if self.current_clicks >= gear.cost:
			gear.quantity += 1
			self.current_clicks -= gear.cost
			gear.cost = int(gear.cost * 1.1) + 1
			self.current_click_label.config(text='{:,}'.format(self.current_clicks))
			if gear.limit and gear.quantity >= gear.limit:
				gear.button.config(state=tk.DISABLED)
				gear.button.config(
						text=gear.button['text'].split(':')[0] + ': {} (MAX)'.format(gear.quantity))
			else:
				gear.button.config(
						text=gear.button['text'].split(':')[0] + ': {}: {}'.format(gear.cost, gear.quantity))

	def update(self):
		per_second = base_per_second = sum(gear.per_second*gear.quantity*(
			gear.multiplier and 2**gear.multiplier.quantity or 1) for gear in self.gear.values())
		for gear in self.gear.values():
			if gear.synergy_unlocked and gear.synergy_unlocked.quantity:		#objects are truthy	
				per_second += gear.quantity * gear.synergy_building.quantity * 0.05 * base_per_second
		self.current_clicks += int(per_second)
		self.current_click_label.config(text='{:,}'.format(self.current_clicks))
		self.per_second_label.config(text='{:,}'.format(int(per_second)))
		self.parent.after(1000, self.update)	#schedule to run itself again in 1s


root = tk.Tk()
clicker = Clicker(root)
root.mainloop()
