import tkinter as tk
from idlelib.tooltip import Hovertip as tip

class Gear:
	def __init__(self, name, description, tooltip, cost, quantity=0, per_second=0, limit=0):
		self.name = name
		self.description = description
		self.tooltip = tooltip
		self.cost = cost
		self.quantity = quantity
		self.per_second = per_second
		self.limit = limit
class Clicker:
	def __init__(self, parent):
		self.parent = parent
		self.purchase_buttons = {}
		self.tooltips = {}
		self.the_button = tk.Button(parent, text='Click the button', width=20, height=5, command=self.increment)	
		self.current_clicks = 0
		self.gear = {}
		self.building = {}
		self.gear['clicker'] = Gear('clicker', 'Clicks per click: (%d): 1', 'Click again whenever you click.', 10, quantity=1, limit=100)
		self.gear['click booster'] = Gear('click booster', 'Multiplicative click booster: (%d) : 0)', 'Doubles your clicks.', 50, limit=5)
		self.gear['noob clicker'] = Gear('noob clicker', 'Noob clicker: (%d): 0', 'A noob at clicking, but they care!', 15, per_second=1)
		self.gear['gremlin'] = Gear('gremlin', 'A gremlin to click things: (%d): 0', 'Gremlins enjoy clicking. Really.', 50, per_second=5)
		self.gear['goblin'] = Gear('goblin', 'A goblin to provide you with clicks: (%d): 0', 'Goblins click more than gremlins.', 200, per_second=30)
		self.gear['inclined plane'] = Gear('inclined plane','Roll some clicks your way: (%d): 0', 'Observe clicks in slow motion.', 500, per_second=125)
		self.gear['pulley'] = Gear('pulley', 'Pull some clicks to you: (%d): 0', 'Not frictionless.', 2000, per_secodn=750)
		self.gear['lever'] = Gear('lever', 'Pry some clicks up: (%d): 0', 'Archimedes would be proud.', 10000, per_second=5000)
		self.gear['wedge'] = Gear('wedge', 'Stuff some extra clicks in there: (%d): 0', 'Can I axe you a question?', 100000, per_second=75000)
		self.gear['elbow grease'] = Gear('elbow grease', 'Click the old fashioned way: (%d): 0', 'Surprisingly easy.', 500000, per_second=500000)

		for gear in (self.gears):
			self.purchase_buttons[name] = tk.Button(parent,
																	text=description % self.gear[name].cost, command=lambda x=name: self.purchase(x))
																	#x=name to define when defined, instead of defined while called	
			self.tooltips[name]= tip(self.purchase_buttons[name], tip)
		
		self.current_click_label = tk.Label(parent, text='0')
		self.the_button.grid(row=0, column=0)
		self.current_click_label.grid(row=0, column=1, columnspan=2)
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
			self.purchase_buttons[name].grid(row=row, column=column)
		
		self.update()
	
	def increment(self):
		self.current_clicks += self.gear['clicker'].quantity * 2**self.gear['click booster'].quantity
		self.current_click_label.config(text='%d' % self.current_clicks)

	def purchase(self, name):
		if self.current_clicks >= self.gear[name].cost:
			self.gear[name].quantity += 1
			self.current_clicks -= self.gear[name].cost
			self.gear[name].cost *= 1.1
			self.current_click_label.config(text='%d' % self.current_clicks)
			self.purchase_buttons[name].config(
				text=self.purchase_buttons[name]['text'].split(':')[0] + ': {:.1f}: {}'.format(self.gear[name].cost,
																													self.gear[name].quantity))
			if self.gear[name].limit and self.gear[name].quantity >= self.gear[name].limit:
				self.purchase_buttons[name].config(state=tk.DISABLED)

	def update(self):
		for gear in self.gear.values():
			self.current_clicks += gear.per_second*gear.quantity
		self.current_click_label.config(text='%d' % self.current_clicks)
		self.parent.after(1000, self.update)


root = tk.Tk()
clicker = Clicker(root)
root.mainloop()
