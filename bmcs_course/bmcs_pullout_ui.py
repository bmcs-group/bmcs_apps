import numpy as np

def plot_filled_var(ax, xdata, ydata, xlabel='', ylabel='', 
                    color='black', alpha=0.1, ylim=None, xlim=None):
    line, = ax.plot(xdata, ydata, color=color);
    if xlabel:
        ax.set_xlabel(xlabel); 
    if ylabel:
        ax.set_ylabel(ylabel)
    if ylim:
        ax.set_ylim(*ylim)
    if xlim:
        ax.set_xlim(*xlim)
    ax.fill_between(xdata, ydata, color=color, alpha=alpha);
    return line

def clear_plot(*axs):
    for ax in axs:
    	ax.collections.clear()

def update_filled_plot(ax, line, xdata, ydata, color='green', alpha=0.1):
    line.set_ydata(ydata)
    line.set_xdata(xdata)
    ax.set_xlim(np.min(xdata), np.max(xdata))
    ax.fill_between(xdata, ydata, 0, color=color, alpha=alpha)

import ipywidgets as ipw
import traits.api as tr
import matplotlib.pyplot as plt

class PlotModel(tr.HasTraits):
    itr = tr.WeakRef
    
    def init_plot(self, model):
        self.model = model
        itr = self.itr
        values = itr.trait_get(interact=True)
        params = list( values[py_var] for py_var in itr.py_vars[1:])
        eps_max = self.model.get_eps_f_x(0,itr.w_max,*params)
        eps_min = self.model.get_eps_m_x(0,itr.w_max,*params)
        tau_max = float(itr.tau * 2)
        w_range = itr.w_range
        x_range = itr.x_range
        w_max = itr.w_max
        L_b = itr.L_b
        self.line_u_f = plot_filled_var(itr.ax_u, x_range, model.get_u_fa_x(x_range,0,*params),
                                 color='brown', alpha=0.2
                                )

        self.line_u_m = plot_filled_var(itr.ax_u, x_range, 
                                        model.get_u_ma_x(x_range,0,*params),
                                 xlabel='$x$ [mm]', ylabel='$u$ [mm]', 
                                 color='black', alpha=0.2, 
                                 ylim=(0, w_max), xlim=(-L_b,0)
                                )

        self.line_eps_f = plot_filled_var(itr.ax_eps, x_range, 
                                          model.get_eps_m_x(x_range, 0,*params),
                                   xlabel='$x$ [mm]', ylabel=r'$\varepsilon$ [mm]', color='green',
                                   ylim=(eps_min, eps_max), xlim=(-L_b,0)
                                  )

        self.line_eps_m = plot_filled_var(itr.ax_eps, x_range, 
                                          model.get_eps_f_x(x_range, 0,*params),
                                   xlabel='$x$ [mm]', ylabel=r'$\varepsilon$ [mm]', color='green',
                                   ylim=(eps_min, eps_max), xlim=(-L_b,0)
                                  )

        self.line_tau = plot_filled_var(itr.ax_tau, x_range, 
                                        model.get_tau_x(x_range, 0,*params),
                                   xlabel='$x$ [mm]', ylabel=r'$\tau$ [MPa]', color='red',
                                   ylim=(0, tau_max), xlim=(-L_b,0)
                                  )

        self.line_po = plot_filled_var(itr.ax_po, w_range, 
                                       model.get_Pw_pull(w_range, *params),
                        xlabel=r'$w$ [mm]', ylabel=r'$P$ [N]', color='blue')
        self.Pw_marker, = itr.ax_po.plot(0,0,marker='o', color='blue')

    def update(self, w, *params):
        model = self.model
        itr = self.itr
        w_range = itr.w_range
        x_range = itr.x_range
        Pw = model.get_Pw_pull(w_range, *params)
        self.P_max = Pw[-1]
        update_filled_plot(itr.ax_po, self.line_po, w_range, Pw,
                           color='blue', alpha=0.1)

        P = model.get_Pw_pull(w, *params)
        self.Pw_marker.set_ydata(P)
        self.Pw_marker.set_xdata(w) 
        u_ma_x = model.get_u_ma_x(x_range,w,*params)
        u_fa_x = model.get_u_fa_x(x_range,w,*params)
        self.u_max = u_fa_x[-1]
        self.u_min = u_ma_x[-1]
        eps_f_x = model.get_eps_f_x(x_range, w,*params)
        eps_m_x = model.get_eps_m_x(x_range, w,*params) 
        self.eps_max = eps_f_x[-1]
        self.eps_min = eps_m_x[-1]
        tau_x = model.get_tau_x(x_range, w,*params)

        update_filled_plot(itr.ax_u, self.line_u_f, x_range, u_fa_x,
                           color='brown', alpha=0.2)
        update_filled_plot(itr.ax_u, self.line_u_m, x_range, u_ma_x,
                           color='black', alpha=0.2)
        update_filled_plot(itr.ax_eps, self.line_eps_m, x_range, eps_m_x, 
                           color='green')
        update_filled_plot(itr.ax_eps, self.line_eps_f, x_range, eps_f_x, 
                           color='green')
        update_filled_plot(itr.ax_tau, self.line_tau, x_range, tau_x, 
                           color='red')

class ModelInteract(tr.HasTraits):

    models = tr.List([
    ])

    py_vars = tr.List(tr.Str)
    map_py2sp = tr.Dict
    
    # define the free parameters as traits with default, min and max values
    w = tr.Float(0.0001, min=1e-5, max=1, interact=True)
    tau = tr.Float(0.5, min=0.01, max=10, interact=True)
    L_b = tr.Float(200, min=0.01, max=1000, interact=True)
    E_f = tr.Float(100000, min=0.01, max=300000, interact=True)
    A_f = tr.Float(20, min=0.01, max=100, interact=True)
    p = tr.Float(40, min=0.01, max=100, interact=True)
    E_m = tr.Float(26000, min=0.01, max=30000, interact=True)
    A_m = tr.Float(100, min=0.01, max=1000, interact=True)

    w_max = tr.Property
    def _get_w_max(self):
        w_trait = self.trait('w')
        return w_trait.max

    w_range = tr.Array(np.float_)
    def _w_range_default(self):
        return np.linspace(0,self.w_max,50)
  
    x_range = tr.Property(tr.Array(np.float_), depends_on='L_b')
    @tr.cached_property
    def _get_x_range(self):
        return np.linspace(-self.L_b,0,100)
  
    def init_plot(self):
        self.fig, ((self.ax_po, self.ax_u),(self.ax_eps, self.ax_tau)) = plt.subplots(
            2,2,figsize=(9,5), tight_layout=True
        )
        self.model_plots = []
        for model in self.models:
            model_plot = PlotModel(itr=self)
            model_plot.init_plot(model)
            self.model_plots.append(model_plot)

    def clear(self):
        clear_plot(self.ax_po,self.ax_u, self.ax_eps,self.ax_tau)

    def update_plot(self, w, **values):
        self.trait_set(**values)
        params = list( values[py_var] for py_var in self.py_vars[1:])
        
        self.clear()
        for model_plot in self.model_plots:
            model_plot.update(w, *params)

        P_max = np.max(np.array([m.P_max for m in self.model_plots]))
        self.ax_po.set_ylim(0, P_max*1.1)
        u_min = np.min(np.array([m.u_min for m in self.model_plots]))
        u_max = np.max(np.array([m.u_max for m in self.model_plots] + [1]))
        self.ax_u.set_ylim(u_min, u_max*1.1)
        eps_min = np.min(np.array([m.eps_min for m in self.model_plots]))
        eps_max = np.max(np.array([m.eps_max for m in self.model_plots]))
        self.ax_eps.set_ylim(eps_min, eps_max*1.1)
        self.ax_tau.set_ylim(0, self.tau*1.1)

        self.fig.canvas.draw_idle()

    n_steps = tr.Int(50)
    def get_ipw_sliders(self):
        traits = self.traits(interact=True)
        vals = self.trait_get(interact=True)
        return { name : ipw.FloatSlider(value=vals[name],
                                        min=trait.min,
                                        max=trait.max,
                                        step=trait.max/self.n_steps,
                                        description=r'\(%s\)' % self.map_py2sp[name].name)
            for (name, trait) in traits.items()
        }        

    def interact(self):
        self.init_plot()
        sliders = self.get_ipw_sliders()
        out = ipw.interactive_output(self.update_plot, sliders);
        layout = ipw.Layout(grid_template_columns='1fr 1fr')
        sliders_list = [sliders[py_var] for py_var in self.py_vars]
        grid = ipw.GridBox(sliders_list, layout=layout)
        box = ipw.VBox([grid, out])
        display(box)

