import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
class Mollweide:
	def __init__(self, rowcol=(1,1), grid=False, ticks=True, locator=ticker.MaxNLocator(), supertitle='', ticksfontdict={}, 
							supertitlefontdict={}, titlefontdict={}, cbar_ax_dict={}, cbar_dict={}):
		self.row, self.col=rowcol
		self.grid = grid 
		self.ticks = ticks
		self.supertitle   = supertitle
		self.cbar_ax_dict = cbar_ax_dict
		self.cbar_dict = cbar_dict
		self.data        = {}
		self.figsize     = (rowcol[1]*6.4,rowcol[0]*3.6)
		self.plotdict    = [dict(locator=locator) for i in range(rowcol[0]*rowcol[1])]
		self.ticksfontdict = {'size':16} # {'family': 'Times New Roman', 'style': 'normal', 'weight': 'normal', 'color':  'black', 'size': 16}
		self.titlefontdict = {'size':35} # {'family': 'calibri', 'style': 'italic', 'weight': 'normal', 'color':  'black', 'size': 35}
		self.supertitlefontdict = {'size':35} # {'serif': 'calibri', 'style': 'italic', 'weight': 'normal', 'color':  'black', 'size': 35}
		self.ticksfontdict.update(ticksfontdict)
		self.titlefontdict.update(titlefontdict)
		self.supertitlefontdict.update(supertitlefontdict)

	def subplots(self, i, j, k, theta, phi, value, title=None, **dic):
		self.data[(i, j, k)] = {'x':phi, 'y':theta, 'z':value, 'title':title}
		self.plotdict[k-1].update(dic)

	def add_plotdict(self, k, **dic):
		self.plotdict[k-1].update(dic)
		
	def show(self, usetex=False, savefile=None, dpi=None):
		fig, axes = plt.subplots(self.row, self.col, figsize=self.figsize, gridspec_kw={'width_ratios': [1, 1, 1.2]})

		if usetex:
			plt.rc('text', usetex=True)
			plt.rc('font', family='calibri', weight='bold')
			plt.rc('text.latex', preamble=[r'\boldmath'])
			# plt.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}', r'\usepackage{bm}', r'\usepackage{gensymb}', r'\boldsymbol']
			# plt.rcParams['text.latex.preamble'] = [r'\boldmath']
		if self.supertitle:
			fig.suptitle(self.supertitle, **self.supertitlefontdict)
		R   = 10
		for i, j, k in self.data.keys():
			phis, thetas = self.data[(i, j, k)]['x'], self.data[(i, j, k)]['y']
			phis, thetas = np.meshgrid(phis, thetas)
			x = R * phis * np.sin(thetas)/np.pi
			y = R * 0.75 * np.cos(thetas)	
			z = self.data[(i,j,k)]['z']
			edgex = R*np.sin(np.linspace(0, np.pi, 100))
			edgey = R*0.75*np.cos(np.linspace(0, np.pi, 100))

			# ax = plt.subplot(i, j, k, alpha=0)
			ax = axes[(k-1)//self.col, (k-1)%self.col]
			# print(self.plotdict[k-1])
			for m in range(10):
				key1 = 'func{}'.format(m)
				key2 = 'arg{}'.format(m)
				if key1 in self.plotdict[k-1]:
					self.plotdict[k-1][key1](ax, **(self.plotdict[k-1].get(key2, {})))
			fmt=self.plotdict[k-1].get('fmt', ticker.ScalarFormatter())
			# print(fmt)
			self.plotdict[k-1].pop('fmt', None)
			bar=ax.contourf(x, y, z, alpha=0.75, **self.plotdict[k-1])
			if k%3==0:
				# ax.Axes(fig, rect=(0.9, 0.8), sharex=True)
				cbar = plt.colorbar(bar, ax=ax, format=fmt, **self.cbar_dict)# pad=0.01, pad=0.01,
				cbar.ax.tick_params(**self.cbar_ax_dict)
				cbar.ax.minorticks_off()
			# c=plt.contour(x,y,z,8,colors='k')
			# ax.set_title(title) 			
			# ax.clabel(c,inline=True,fontsize=10)

			ax.set_xlim(-R-0.5, R+0.5)
			ax.set_ylim(-R, R)
			ax.set_axis_off()
			ax.plot( edgex, edgey, 'k')
			ax.plot(-edgex, edgey, 'k')
			if self.grid:
				theta_temp = np.linspace(0, np.pi, 100)
				phi_temp = np.linspace(-np.pi, np.pi, 100)
				grid_color = 'grey'
				for phi in np.array([-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150])*np.pi/180:
					x = R * phi * np.sin(theta_temp)/np.pi
					y = R * 0.75 * np.cos(theta_temp)
					ax.plot(x, y, grid_color, alpha=0.3)
				for theta in np.array([15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165])*np.pi/180:
					x = R * phi_temp * np.sin(theta)/np.pi
					y = np.full(len(phi_temp), R * 0.75 * np.cos(theta))
					ax.plot(x, y, grid_color, alpha=0.3)
			if self.ticks:
				for ps in range(-5, 6, 2): 
					tick = r'%d$^\circ$'% (30*ps)
					ax.text(R/6*ps, 0, tick, fontdict=self.ticksfontdict, ha='center', va='center_baseline')
				# poffset = [0.02, 0.02, 0.06, 0.1, 0.13]
				# offset = np.array(poffset+[0]+poffset[::-1])*R
				for ps in range(-5, 6):
					if ps<0:
						tick = r'-%d$^\circ$'% (-15*ps)
						ax.text(-R*np.cos(np.pi/12*ps) + 0.24*R*(np.cos(np.pi/15*ps - 0.15*np.pi)-1), R*0.75*np.sin(np.pi/12*ps), tick, fontdict=self.ticksfontdict, ha='right', va='center_baseline')
					elif ps>0:
						tick = r'%d$^\circ$'% (15*ps)
						ax.text(-R*np.cos(np.pi/12*ps) + 0.24*R*(np.cos(np.pi/15*ps + 0.15*np.pi)-1), R*0.75*np.sin(np.pi/12*ps), tick, fontdict=self.ticksfontdict, ha='right', va='center_baseline')
					else:
						ax.text(-1.05*R, 0, r'$0^\circ$', fontdict=self.ticksfontdict, ha='right', va='center_baseline')
			ax.text(0, R*0.8, self.data[(i,j,k)]['title'], fontdict=self.titlefontdict, ha='center', va='bottom')
		fig.patch.set_alpha(0)
		plt.subplots_adjust(left=0.07, right=0.92, bottom=0.07, top=0.97)
		if not savefile:
			plt.show()
		else:
			plt.savefig(savefile, dpi=dpi)