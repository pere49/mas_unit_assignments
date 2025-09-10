import numpy as np
import matplotlib.pyplot as plt

# Set print options for numpy arrays
np.set_printoptions(precision=3, suppress=True)

class ThinCylinder:
    def __init__(self, P_i, P_o, r_i, threshold=0.01, n=3000):
        self.P_i = P_i # Inner pressure in MPa
        self.P_o = P_o # Outer pressure in MPa
        self.r_i = r_i # Inner radius in meters
        self.s_ratio = 0.0 # Stress ratio
        self.threshold = threshold # Threshold for acceptable error in hoop stress approximation
        self.n = n # Number of points for calculations

    def lame_stress(self, r_i, r_o, p_i, p_o):
        """Calculate hoop stresses in a thick-walled cylinder using Lame's equations."""
        A = (p_i * r_i**2 - p_o * r_o**2) / (r_o**2 - r_i**2)
        B = ((p_i - p_o)*(r_i**2 * r_o**2 )) / (r_o**2 - r_i**2)
        return A + B / r_i**2
    
    def thin_approx(self, r_i, r_o, p_i, p_o):
        """ calculate the hoop stresses in a thin-walled cylinder using approximate equations."""
        r = (r_o + r_i) / 2 # Average radius
        t = (r_o - r_i)  # Wall thickness
        return (p_i - p_o) * r / t
        
    
    def find_s_ratio(self):
        """This function calculates the radius ratio 's' for which the hoop stress
        approximation error is less than 1%.
        The function uses a range of thickness values to compute the outer radius
        and then calculates the radius ratio."""
        r_i = self.r_i  # inner radius in meters
        t = np.linspace(0.001, 0.3, self.n)  # thickness in meters
        r_o = r_i + t  # outer radius
        s = r_o / r_i  # radius ratio

        exact = self.lame_stress(r_i, r_o, self.P_i, 0)
        approx = self.thin_approx(r_i, r_o, self.P_i, 0)
        error = np.abs(exact - approx) / exact  # percentage error
        self.s_ratio = s[error < self.threshold]  # condition for acceptable error
        critical_s = self.s_ratio[-1] if len(self.s_ratio) > 0 else None
        print(f"Radius ratio 's' for which error is less than 1%: {self.s_ratio}")
        print(f"Critical radius ratio 's' for acceptable error: {critical_s}")

        plt.plot(s, error, label='error ratio', color='b')
        plt.scatter(self.s_ratio[-1],self.threshold, label=f"critical ratio:{critical_s:.2f}", marker='x', color='k',zorder=1)
        plt.xlabel('Radius Ratio (s)')
        plt.ylabel('Percentage Error (%)')
        plt.title('Error in Hoop Stress Approximation')
        plt.legend()
        plt.grid()
        plt.show()

    def error_against_pressure(self, r_i):
        """This function calculates the error in hoop stress approximation against pressure."""
        p_i = self.P_i  # inner pressure in MPa
        p_o = np.linspace(1, p_i*.83, self.n)  # outer pressure in MPa
        p_magnitude = np.abs(p_i - p_o) / ((p_o + p_i)/2)  # magnitude of pressure difference

        for s in self.s_ratio[1::500]:  # Iterate through radius ratios
            r_o = s * r_i
            exact = self.lame_stress(r_i, r_o, p_i, p_o)
            approx = self.thin_approx(r_i, r_o, p_i, p_o)
            error = np.abs(exact - approx) / exact
            plt.plot(p_magnitude, error, label=f's = {s:.2f}')

        plt.xlabel('Magnitude of Pressure Difference')
        plt.ylabel('Percentage Error (%)')
        plt.title('Error in Hoop Stress Approximation vs Pressure Difference')
        plt.legend()
        plt.grid()
        plt.show()
        

P_i = 100  # Inner pressure in Pascals
P_o = 0  # Outer pressure in Pascals
r_i = 1  # Inner radius in meters


cylinder = ThinCylinder(P_i, P_o, r_i)
cylinder.find_s_ratio()  # Find radius ratio for acceptable error
cylinder.error_against_pressure(r_i)  # Plot error against pressure