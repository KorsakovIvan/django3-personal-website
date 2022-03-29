# Generate 10 separate random flips with probability 30%:
rbinom(10, 1, .3)

# Generate 100 occurrences of flipping 10 coins, each with 30% probability:
rbinom(100, 10, .3)

# Calculate the probability that 2 are heads
# using dbinom:
dbinom(2, 10, .3)

# using rbinom:
mean(rbinom(10000, 10, .3)==2)

# Calculate the probability that at least five coins are heads
# using pbinom:
1-pbinom(4, 10, .3)

# using simulation of 10,000 trials:
mean(rbinom(10000, 10, .3) >= 5)

# Calculating expected value and variance of a binomial distribution
# Expected value = size * p
# Variance = size * p * (1 - p)

# Calculate the expected value:
# 25 coins are flipped, each having a 30% chance of heads
# using the exact formula:
eval_exact <- 25 * .3

# using rbinom:
mean(rbinom(10000,25,.3))

# Calculate the variance
# using the exact formula:
var_exact <- 25 * .3 * (1 - .3)

# using rbinom
var(rbinom(10000,25,.3))
