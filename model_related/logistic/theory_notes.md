### logit function relation to logistic regression equation

\[
\begin{aligned}
\text{logit}(p) &= \log\!\left(\frac{p}{1-p}\right) \\
\log\!\left(\frac{p}{1-p}\right) &= \beta_0+\beta_1 x \\
\frac{p}{1-p} &= e^{\beta_0+\beta_1 x} \\
p &= (1-p)e^{\beta_0+\beta_1 x} \\
p + pe^{\beta_0+\beta_1 x} &= e^{\beta_0+\beta_1 x} \\
p\left(1+e^{\beta_0+\beta_1 x}\right) &= e^{\beta_0+\beta_1 x} \\
p &= \frac{e^{\beta_0+\beta_1 x}}{1+e^{\beta_0+\beta_1 x}} \\
p &= \frac{1}{1+e^{-(\beta_0+\beta_1 x)}}
\end{aligned}
\]


