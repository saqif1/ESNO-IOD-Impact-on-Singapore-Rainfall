import matplotlib.pyplot as plt

# Define the coefficients and their labels
coefs = [0.8569, 0.5188, 0.3382, 0.3339]
labels = ['ENSO_LN', 'ENSO_Neutral', 'IOD_-IOD', 'IOD_Neutral']

# Define the corresponding p-values
p_values = [0.001, 0.012, 0.102, 0.047]

# Set the plot style
plt.style.use('seaborn')

# Create the bar plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(labels, coefs, color=['tab:blue', 'tab:orange', 'tab:green', 'tab:red'])
ax.axhline(y=0, color='black', linewidth=0.5)
ax.set_ylabel('Coefficient')
ax.set_xlabel('ENSO and IOD categories')
ax.set_title('Coefficients from Multiple Linear Regression Analysis')
ax.tick_params(axis='x', rotation=45)
ax2 = ax.twinx()
ax2.plot(labels, p_values, marker='o', color='tab:purple')
ax2.set_ylim(0, 0.15)
ax2.set_ylabel('p-value')
ax2.grid(False)

# Show the plot
#plt.show()






































