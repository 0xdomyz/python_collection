
> Logistic regression is a GLM where:
> - The response variable \( Y_i \in \{0, 1\} \) is modeled as a Bernoulli random variable.
> - The mean of this distribution, \( \mathbb{E}[Yi] = pi \), is related to the linear predictor \( \etai = Xi \beta \) via the logit link:
>   \[
>   \log\left(\frac{pi}{1 - pi}\right) = X_i \beta
>   \]
> - This setup allows us to model probabilities using a linear combination of predictors, while ensuring outputs stay in \((0, 1)\).
> - Parameters \( \beta \) are estimated via maximum likelihood, not least squares.
