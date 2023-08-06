
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import wuml

class regression:
	def __init__(self, data, y=None, y_column_name=None, split_train_test=True, regressor='GP', kernel=None):

		if y is not None:
			y = wuml.ensure_numpy(y)

		elif y_column_name is not None:
			y = data[y_column_name].values
		elif type(data).__name__ == 'wData':
			y = data.Y
		else:
			raise ValueError('Undefined label Y')

		X = wuml.ensure_numpy(data)

		if regressor == 'GP':
			model = GaussianProcessRegressor(kernel=kernel, random_state=0)
			model.fit(X, y)
			[self.ŷ, self.σ] = model.predict(X, return_std=True)
			self.mse = mean_squared_error(y, self.ŷ)

		self.model = model
		self.regressor = regressor

	def __call__(self, data):
		X = wuml.ensure_numpy(data)	

		if self.method == 'GP' or self.method == 'KPCA':
			[self.ŷ, self.σ] = model.predict(X, return_std=True)

			output = self.model.predict(X, return_std=True, return_cov=False)
			import pdb; pdb.set_trace()
			return wuml.ensure_data_type(output, type_name=type(data).__name__)
		else:
			raise ValueError('Regressor not recognized, must use regressor="GP"')
		

	def __str__(self):
		s = 'Regressor: %s\n'%self.regressor
		s += 'MSE : %.4f\n'%self.mse
