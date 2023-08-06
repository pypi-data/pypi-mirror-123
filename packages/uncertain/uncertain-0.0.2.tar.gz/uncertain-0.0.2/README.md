# UNCERTAIN
Python module to keep track of uncertainties in mathematical calculations.


## Usage example
Input:


```
from uncertain import *
a = UncertainValue(5, 3, 8, 'normal', [5, 1])
b = UncertainValue(1, 0.1, 4)
c = -b+2*a**(b/3)

print(c.describe(),
    "\n\nThe standard deviation of b is "+str(b.std),
	"\n\nThe probability of /c/ being between 2 and 6 is " +
	str(probability_in_interval(c, [2, 6])))

a.plot_distribution(title="Uncertain numbers", label="a")
b.plot_distribution(label="b", alpha=0.5)
c.plot_distribution(label="c", alpha=0.5)

c.plot_distribution(plot_type='cdf', new_figure=True)
```


Output:


```
This variable is an uncertain value. It has the following properties:

	- Nominal value: 2.4199518933533937

	- Mean: 5.1973349566661415
	- Median: 3.8063419262133795
	- Variance: 13.086116036143682
	- Standard deviation: 3.6174737091157527
	- Skewness: 1.5519941650511524

	- Lower bound: -1.9254016053940988
	- Percentile 5: 2.0248565203431506
	- Q1: 2.432100693608657
	- Q3: 6.832833238201248
	- Percentile 95: 12.808458201483177
	- Upper bound: 31.899999999999995

	- Probability distribution type: custom
	- Number of samples: 100000
 

The standard deviation of b is 1.1245368594834484 

The probability of /c/ being between 2 and 6 is 0.67164
```

![Probability density](./resources/density_plot.png)  
![Cumulative density](./resources/cdf_plot.png)
