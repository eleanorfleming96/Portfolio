# What is Optimization?

**Optimization** is the process of finding the best solution to a problem from a set of possible solutions. It involves choosing the values of certain variables (called **decision variables**) to either:

- **Maximize** something desirable (like profit, efficiency, or happiness), and/or  
- **Minimize** something undesirable (like cost, time, or waste)  

while satisfying certain **constraints** (rules or limits) imposed by the problem.

---

<details>
  <summary> Single Objective Example: Maximizing Profit (Simple Case)</summary>

Imagine you're a farmer with 10 acres of land. You can plant **wheat** or **corn**:

- Wheat gives **$100 profit per acre**.
- Corn gives **$150 profit per acre**.
- Your goal is to **maximize profit**, but you only have 10 acres to work with.

### Variables
- `w`: Acres of wheat planted.  
- `c`: Acres of corn planted.  

### Objective
- Maximize profit:  
  `p(w, c) = 100w + 150c`

### Constraint
- Total land available:  
  `w + c <= 10`

---

### Solution Intuition

Corn is more profitable, so to maximize profit, you should plant all 10 acres with corn. This gives the highest possible profit:  
`p(0, 10) = 150 * 10 = 1500`

</details>

---

<details>
  <summary> Multi-Objective Example: Maximizing Profit and Minimizing Water Usage</summary>

Now let’s add another consideration: **water is scarce**. Corn uses **4 units of water per acre**, while wheat uses only **2 units per acre**. You now have two objectives:

1. **Maximize profit**:  
   `p(w, c) = 100w + 150c`

2. **Minimize water usage**:  
   `h(w, c) = 2w + 4c`

---

### The Trade-Off

Corn gives more profit but uses more water. Wheat uses less water but gives lower profit. You can’t do both perfectly, so you need to find a **balance**.

---

### Balancing Profit and Water Usage

To balance these goals, you combine them into a single formula:  
`z(w, c) = alpha * p(w, c) - beta * h(w, c)`

Here:
- `alpha`: Weight for profit (how important profit is).  
- `beta`: Weight for water conservation (penalty for water usage).

The weights `alpha` and `beta` in the formula act as scalars that determine the relative importance of the two objectives. For example, if `alpha = 2` and `beta = 1`, you are telling the objective function that maximizing profit is twice as important as minimizing water consumption.

---

### Key Scenarios

- **If profit is more important (`alpha > beta`)**:  
  Plant mostly corn to maximize profit, even if water usage is higher.

- **If water conservation is more important (`beta > alpha`)**:  
  Plant mostly wheat to use less water, even if profit is lower.

---

### Example Objective Weights and Outcomes

1. **Maximizing Profit (`alpha = 1, beta = 0.1`)**:  
   Focus on profit. Plant all 10 acres with corn:  
   - Profit: $1500  
   - Water usage: 40 units.

2. **Balancing Both (`alpha = 1, beta = 0.5`)**:  
   Balance profit and water use. Split land (4 acres wheat, 6 acres corn):  
   - Profit: $1300  
   - Water usage: 32 units.

3. **Minimizing Water (`alpha = 1, beta = 1`)**:  
   Focus on water conservation. Plant all 10 acres with wheat:  
   - Profit: $1000  
   - Water usage: 20 units.

---

### Insights

Optimization often involves trade-offs. By adjusting weights (`alpha, beta`), you can explore how much you prioritize one goal over another. This approach allows you to find the solution that best fits your overall needs.

</details>

---

<details>
  <summary> Equity Portfolio Optimization: Maximizing ESG Ratings and Minimizing Risk </summary>

Let’s apply these principles to **portfolio optimization**, which is used to build or adjust a mix of investments (like stocks or other securities) to meet specific goals and rules. Tools like **Aladdin** help investors set up this problem by defining their **goals** and **constraints**. Then, the tool finds the **best mix of investments** that satisfies all these requirements.

## **Portfolio Optimization Problem**

Imagine you currently hold the following portfolio of 5 stocks:

| **Stock** | **Current Weight** | **New Weight (xᵢ)** | **ESG Score (eᵢ)** | **Risk/Volatility (σᵢ)** | **Sector**       |  
|-----------|--------------------|---------------------|--------------------|--------------------------|------------------|  
| A         | 25% (0.25)         | x₁                  | 90                 | 8%                       | Technology       |  
| B         | 20% (0.2)          | x₂                  | 80                 | 6%                       | Energy           |  
| C         | 15% (0.15)         | x₃                  | 70                 | 5%                       | Healthcare       |  
| D         | 20% (0.2)          | x₄                  | 85                 | 7%                       | Energy           |  
| E         | 20% (0.2)          | x₅                  | 60                 | 4%                       | Consumer Goods   |  


Here:  
- **Current Weight** represents your initial allocation to each stock.  
- You can **buy or sell** to adjust these weights, but they must still add up to 100% (1.0).
- The **decision variables** `x₁, x₂, x₃, x₄, x₅` are the updated portfolio weights. They represent the new proportions of your budget invested in Stocks A, B, C, D, and E after optimizing.  

### Objective Function: Balancing ESG Scores and Risk  

Your goal with this portfolio is to **maximize ESG scores** while **minimizing portfolio risk**: 

1. **Maximizes ESG scores** (`e`) – focuses on sustainable and socially responsible investments.  
2. **Minimizes risk** (`r`) – reduces the chance of large fluctuations in returns (**volatility**).  

Using the following function:

`z(x) = alpha * e(x) - beta * r(x)`  

Where:  
- `e(x) = Sum(e_i * x_i)` (weighted sum of ESG scores).  
- `r(x) = Sum(sigma_i * x_i)` (weighted sum of asset volatilities).  
- `alpha`: Weight for ESG scores (importance of sustainability).  
- `beta`: Weight for risk (importance of reducing volatility).  
 
---

### **Constraints**
While trying to achieve your goal, you need to maintain certain constraints.

1. **Energy Sector Allocation**:  
   Stocks B and D (Energy) must make up at least 15% of the portfolio:  
  x₂ + x₄ ≥ 0.15

2. **Non-Negativity**:  
  You can’t sell short, so all weights must be non-negative:  
x₁, x₂, x₃, x₄, x₅ ≥ 0

3. **Fully Invested**:
   100% of the available investment capital is allocated, in onther words the total weights must sum to 1:  
  x₁ + x₂ + x₃ + x₄ + x₅ = 1

---

### 4. Solve using an Optimization Algorithm  

Optimization solvers use smart algorithms to find the best solution by fine-tuning the decision variables (e.g., `x₁, x₂, ..., x₅`) step by step. They start with an initial guess and gradually improve it until an optimal result is reached.  

1. **Start with a Starting Point**:  
   The solver picks an initial set of values for the variables (e.g., initial weights for a portfolio).  

2. **Make Iterative Adjustments**:  
   The solver tweaks the values slightly and checks:  
   - Does this new combination improve the objective (e.g., higher ESG score or lower risk)?  
   - Are all the rules (constraints) still followed?  

3. **Find the Best Solution**:  
   The solver keeps refining the values until it can’t make meaningful improvements or it meets a set stopping condition (like a tiny improvement threshold).  

---

### Common Approaches  
- **Linear Programming (LP)**:  
   Used when the problem and constraints are simple, straight-line relationships.  
- **Gradient Descent**:  
   A step-by-step method that adjusts the variables by moving in the “best direction” to improve the result as quickly as possible.  

---

In short, solvers act like smart navigators: they explore possible solutions, compare them, and zero in on the best answer while respecting all the given rules.  

Let’s assume the solution is as follows:

| **Stock** | **Current Weight** | **New Weight (xᵢ)** | **Change** |  
|-----------|--------------------|---------------------|------------|  
| A         | 0.25               | 0.2                 | -0.05      |  
| B         | 0.2                | 0.15                | -0.05      |  
| C         | 0.15               | 0.25                | +0.10      |  
| D         | 0.2                | 0.25                | +0.05      |  
| E         | 0.2                | 0.15                | -0.05      |  

---

### Step 5: Evaluate the Solution

1. **Total ESG Score**:  
E(x) = (90 · 0.2) + (80 · 0.15) + (70 · 0.25) + (85 · 0.25) + (60 · 0.15) E(x) = 18 + 12 + 17.5 + 21.25 + 9 = 77.75

2. **Total Risk**:  
V(x) = (8% · 0.2) + (6% · 0.15) + (5% · 0.25) + (7% · 0.25) + (4% · 0.15) V(x) = 1.6% + 0.9% + 1.25% + 1.75% + 0.6% = 6.1%

3. **Objective Function**:  
Z(x) = (2 · 77.75) - (1 · 6.1) = 155.5 - 6.1 = 149.4

---

### Key Takeaway  

This example highlights how portfolio optimization works by **rebalancing existing holdings** to achieve specific goals—**maximizing ESG scores** and **minimizing risk**—while adhering to constraints like sector requirements.  

#### Key Insights:  
1. **Improved ESG and Managed Risk**:  
   By reallocating more funds to higher-ESG stocks, the portfolio achieved a higher total ESG score while keeping the risk increase modest at **6.1%**.  

2. **Constraint Satisfaction**:  
   Energy stocks (B and D) now account for **40%** of the portfolio, exceeding the minimum 15% requirement.  

3. **Efficiency and Flexibility**:  
   Minimal adjustments kept transaction costs low, while tuning weights (e.g., `α` for ESG and `β` for risk) allowed for a balanced trade-off between sustainability and volatility.  

Just as a farmer balances **profit (ESG scores)** and **water usage (risk)**, investors can customize optimization tools like **Aladdin** to seamlessly integrate priorities and constraints, ensuring efficient, data-driven solutions.  

</details>
