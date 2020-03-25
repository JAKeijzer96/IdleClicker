import tkinter as tk
from idlelib.tooltip import Hovertip as tip

class Gear:
	def __init__(self, name, cost, quantity=0, per_second=0, limit=0):
		self.name = name
		self.cost = cost
		self.quantity = quantity
		self.per_second = per_second
		self.limit = limit
class Clicker:
	def __init__(self, parent):
		self.parent = parent
		self.purchase_buttons = {}
		self.the_button = tk.Button(parent, text='Click the button', width=20, height=5, command=self.increment)	
		self.current_clicks = 0
		self.gear = {}
		self.building = {}
		self.gear['clicker'] = Gear('clicker', 10, quantity=1, limit=100)
		self.gear['click booster'] = Gear('click booster', 50, limit=5)
		self.gear['noob clicker'] = Gear('noob clicker', 15, per_second=1)
		self.gear['gremlin'] = Gear('gremlin', 50, per_second=5)

		self.purchase_buttons['clicker'] = tk.Button(parent, text='Clicks per click: (%d) : 1' % self.gear['clicker'].cost, 
			command=lambda: self.purchase('clicker'))
		self.purchase_buttons['click booster'] = tk.Button(parent, text='Multiplicative click booster: (%d) : 0' % self.gear['click booster'].cost,
			command=lambda: self.purchase('click booster'))
		self.purchase_buttons['noob clicker'] = tk.Button(parent, text='Noob clicker: (%d): 0' % self.gear['noob clicker'].cost, 
			command=lambda: self.purchase('noob clicker'))		
		self.purchase_buttons['gremlin'] = tk.Button(parent, text='A gremlin to click things: (%d): 0' % self.gear['gremlin'].cost, 
			command=lambda: self.purchase('gremlin'))
		self.tooltips = {'clicker':tip(self.purchase_buttons['clicker'], 'Click again whenever you click.'),
								'click booster':tip(self.purchase_buttons['click booster'], 'Doubles your clicks.'),
								'noob clicker':tip(self.purchase_buttons['noob clicker'], 'A noob at clicking, but they care!'),
								'gremlin':tip(self.purchase_buttons['gremlin'], 'Gremlins enjoy clicking. Really.')
								}
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
