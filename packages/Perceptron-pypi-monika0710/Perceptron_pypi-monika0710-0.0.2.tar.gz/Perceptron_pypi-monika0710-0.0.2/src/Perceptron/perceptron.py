import numpy as np
class Perceptron:
  def __init__(self,eta,epoch):
    self.eta =eta
    self.epoch=epoch
    self.weight=np.random.randn(3) * 1e-4

  def activationFunction(self,inputs,weight):
    z=np.dot(inputs,weight)
    return np.where(z>0,1,0)
  

  def fit(self,X,y):
    self.X=X
    self.y=y
    X_with_bias=np.c_[self.X,-np.ones((len(self.X),1))]
    print(f"X_with_bias val \n{X_with_bias}")
    
    for epoch in range(self.epoch):
      y_hat=self.activationFunction(X_with_bias,self.weight)
      print(f"y_hat val \n{y_hat}")
      self.error=self.y-y_hat

      self.weight=self.weight+self.eta*np.dot(X_with_bias.T,self.error)
      print(f"weight upation aftr epoch \n{self.weight}")
  # def fit(self, X, y):
  #   self.X = X
  #   self.y = y

  #   X_with_bias = np.c_[self.X, -np.ones((len(self.X), 1))] # CONCATINATION
  #   print(f"X with bias: \n{X_with_bias}")

  #   for epoch in range(self.epochs):
  #     print("--"*10)
  #     print(f"for epoch: {epoch}")
  #     print("--"*10)

  #     y_hat = self.activationFunction(X_with_bias, self.weights) # foward propagation
  #     print(f"predicted value after forward pass: \n{y_hat}")
  #     self.error = self.y - y_hat
  #     print(f"error: \n{self.error}")
  #     self.weights = self.weights + self.eta * np.dot(X_with_bias.T, self.error) # backward propagation
  #     print(f"updated weights after epoch:\n{epoch}/{self.epochs} : \n{self.weights}")
      # print("#####"*10)
  def predict(self,X):
    X_with_bias=np.c_[X,-np.ones((len(X),1))]
    print(f"final wt : \n{self.weight}")
    return self.activationFunction(X_with_bias,self.weight)
    