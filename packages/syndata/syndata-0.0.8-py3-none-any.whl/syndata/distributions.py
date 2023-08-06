"""
This module provides several probability distributions for drawing synthetic
data for clusters.

CLASSES AND METHODS

	GaussianData : draw Gaussian data for cluster
		__init__(self)
		sample_cluster(self,cluster_size,mean,axes,sd)

	ExpData : draw doubly exponentially distributed data for cluster
		__init__(self)
		sample_cluster(self,cluster_size,mean,axes,sd)

	tData : draw Student t-distributed data for cluster
		__init__(self)
		sample_cluster(self,cluster_size,mean,axes,sd)

"""

from .core import DataDist
import numpy as np


class GaussianData(DataDist):
	"""
	Draw Gaussian data for a cluster.

	Attributes
	----------
	None

	Methods
	-------
	__init__(self, ...)
	sample_cluster(self, cluster_size, mean, axes, sd, ...)

	"""

	def __init__(self):
		"""
		Instantiate a GaussianData object.

		"""
		pass

	def sample_cluster(self,cluster_size,mean,axes,sd):
		"""
		Sample a Gaussian cluster.

		cluster_size : int
			The number of data points in this cluster.
		mean : ndarray
			Cluster of this cluster.
		axes : list of ndarray
			Principle axes of this cluster.
		sd : list of float
			Standard deviations of this cluster's principal axes.
		"""

		# assemble covariance matrix
		cov = np.transpose(axes) @ np.diag(sd**2) @ axes
		# sample data
		X = np.random.multivariate_normal(mean=mean, 
									cov=cov, size=cluster_size)
		return X


class ExpData(DataDist):
	"""
	Draw exponentially distributed synthetic data for a cluster.

	Attributes
	----------
	None

	Methods
	-------
	__init__(self, ...)
	sample_cluster(self, cluster_size, mean, axes, sd, ...)

	"""

	def __init__(self):
		"""
		Instantiate an ExpData object.

		"""
		pass

	def sample_cluster(self,cluster_size, mean,axes,sd):
		"""
		Sample an exponentially distributed cluster.

		Sampling is performed using spherical coordinates. First, a random
		point on the unit sphere is sampled. This point is then scaled by 
		a draw from an exponential distribution with standard deviation 1.
		Finally, the point is stretched or compressed along each principal
		axis of the cluster by the corresponding standard deviation.

		cluster_size : int
			The number of data points in this cluster.
		mean : ndarray
			Cluster of this cluster.
		axes : list of ndarray
			Principle axes of this cluster.
		sd : list of float
			Standard deviations of this cluster's principal axes.
		"""

		# each row of axes is an axis
		n_axes = axes.shape[0]

		# sample on the unit sphere
		X = np.random.multivariate_normal(mean=np.zeros(n_axes), cov=np.eye(n_axes), 
										  size=cluster_size)
		X /= np.sqrt(np.sum(X**2,axis=1))[:,np.newaxis]

		# scale sampled unit vectors by draws from standard exponential dist
		X *= np.random.exponential(scale=1,size=cluster_size)[:,np.newaxis]

		# stretch/compress samples along principal axes
		X = X @ np.diag(sd) @ axes

		# translate sampled data to the desired mean
		X = X + mean[np.newaxis,:]

		return X


class tData(DataDist):
	"""
	Draw t-distributed data for a cluster.

	Attributes
	----------
	df : int
		Degrees of freedom in Student t distribution. Low values (e.g. 1) lead
		to heavy tails. For very high values, the distribution becomes Gaussian.

	Methods
	-------
	__init__(self, ...)
	sample_cluster(self, cluster_size, mean, axes, sd, ...)

	"""

	def __init__(self, df=1):
		"""
		Instantiate a tData object.

		Parameters
		----------
		self : tData
			This instance of tData
		df : int
			Degrees of freedom in Student t distribution

		"""
		self.df = df

	def sample_cluster(self,cluster_size, mean,axes,sd,n_empirical_median=1e+6):
		"""
		Sample a t-distributed cluster.

		Sampling is performed using spherical coordinates. First, a random
		point on the unit sphere is sampled. This point is then scaled by 
		a draw from a Student t distribution with self.df degrees of freedom,
		normalized by the median of the absolute value of the same t 
		distribution. Finally, the sampled point is stretched or compressed 
		along each principal axis of the cluster by the corresponding standard
		deviation.

		cluster_size : int
			The number of data points in this cluster.
		mean : ndarray
			Cluster of this cluster.
		axes : list of ndarray
			Principle axes of this cluster.
		sd : list of float
			Standard deviations of this cluster's principal axes.
		n_empirical_median : int, default=1e+6
			Number of samples used to approximate the median of the absolute
			value of the chosen t distribution
		"""

		# compute median for absolute value of t distribution
		n = n_empirical_median
		abs_t_median = np.median(np.abs(np.random.standard_t(df=self.df,size=n)))

		# each row of axes is an axis
		n_axes = axes.shape[0]

		# sample on the unit sphere
		X = np.random.multivariate_normal(mean=np.zeros(n_axes), cov=np.eye(n_axes), 
										  size=cluster_size)
		X /= np.sqrt(np.sum(X**2,axis=1))[:,np.newaxis]

		# scale sampled unit vectors by draw from normalized t-distribution 
		scaling = 1/abs_t_median
		X *= np.random.standard_t(df=self.df, 
				size=cluster_size)[:,np.newaxis] * scaling

		# stretch/compress along principal axes
		X = X @ np.diag(sd) @ axes

		# mean-shift X
		X = X + mean[np.newaxis,:]

		return X