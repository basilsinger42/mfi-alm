import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of policyholders
num_policyholders = 1000

# Generate random values
ages = np.random.randint(20, 81, size=num_policyholders)  # Ages between 20 and 80
benefits = np.random.randint(100000, 2000001, size=num_policyholders)  # Benefits between 100k and 2M
mu_values = np.random.uniform(0.03, 0.08, size=num_policyholders)  # mu between 0.03 and 0.08

# Create DataFrame
policyholder_df = pd.DataFrame({
    "policyholder_id": np.arange(1, num_policyholders + 1),
    "age": ages,
    "benefit": benefits,
    "mu": mu_values
})

# Save to CSV
policyholder_df.to_csv("policyholder_tape.csv", index=False)
