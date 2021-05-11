import numpy as np

SCALE_PARAMS = {"low_bound_gauss": 0.01, "up_bound_gauss": 0.15, "scale": 4}
def noise_aug(noise_type,
              data,
              snr,
              rate,
              snr_thres = 10,
              rate_thres = 1,
              scale_params = None):
     
    '''
    
    noise_type: str
       "additive_gaussian" or "multiplicative_exponential", "multiplicative_rayleigh" or "additive_exponential"
    
    data: 
       data, it can be .hdf5 file or numpy array which will be augmented (for numpy array: it should have three columns.)
       
    snr: float or int
       the ratio of the power of a signal (meaningful or desired input) to the power of noise (meaningless or unwanted input).
       
    rate: float or int
       rate of augmentation
    
    rate_thres: float or int
       rate threshold to be augmented     
       
    snr_thres: float or int
       signal to noise threshold to be augmented.
       
    scale_params: dict (optional) {"low_bound_gauss": None, "up_bound_gauss": None, "scale": None}
       "low_bound_gauss" which determines lower bound of the interval for standard deviation of additive_gaussian function. 
       It is for additive_gaussian and its default value is 0.01.
       
       "up_bound_gauss" which determines upper bound of the interval for standard deviation of additive_gaussian function. 
       It is for additive_gaussian and its default value is 0.15.
       
       "scale" which is scale value for "multiplicative_exponential", "multiplicative_rayleigh" and "additive_exponential" functions and its default value is 4.
       
       
    '''
    
    if scale_params is None:
        scale_params = SCALE_PARAMS
        
    if noise_type == "additive_gaussian":
        noise_augmented = gauss_add_noise(data, snr, rate, snr_thres, rate_thres, scale_params = None)
    elif noise_type == "multiplicative_exponential":
        noise_augmented = exp_mult_noise(data, snr, rate, snr_thres, rate_thres, scale_params = None)
    elif noise_type == "multiplicative_rayleigh":
        noise_augmented = ray_mult_noise(data, snr, rate, snr_thres, rate_thres, scale_params = None)
    elif noise_type == "additive_exponential":
        noise_augmented = exp_add_noise(data, snr, rate, snr_thres, rate_thres, scale_params = None)
    else:
        raise NameError(noise_type  + " " + + "could not be found, enter valid noise_type")
    return noise_augmented


GAUSS_DEFAULT_SCALE_PARAMS = {"low_bound_gauss": 0.01, "up_bound_gauss": 0.15}          
def gauss_add_noise(data, snr, rate, snr_thres, rate_thres, scale_params = None):
    if scale_params is None:
        scale_params = GAUSS_DEFAULT_SCALE_PARAMS
    '''Apply additive Gaussian noise with a random scale variable onto raw waveform data; scale_params = {low_bound_gauss: None, up_bound_gauss: None}'''
    data_noisy = np.empty(data.shape)
    if np.random.uniform(0, rate_thres) < rate and snr >= snr_thres: 
        data_noisy = np.empty((data.shape))
        data_noisy[:, 0] = data[:,0] + np.random.normal(0, np.random.uniform(scale_params["low_bound_gauss"], 
                                                                             scale_params["up_bound_gauss"])*max(data[:,0]), data.shape[0])
        data_noisy[:, 1] = data[:,1] + np.random.normal(0, np.random.uniform(scale_params["low_bound_gauss"], 
                                                                             scale_params["up_bound_gauss"])*max(data[:,1]), data.shape[0])
        data_noisy[:, 2] = data[:,2] + np.random.normal(0, np.random.uniform(scale_params["low_bound_gauss"], 
                                                                             scale_params["up_bound_gauss"])*max(data[:,2]), data.shape[0])    
    else:
        data_noisy = data
    return data_noisy 

EXP_AND_RAY_DEFAULT_SCALE_PARAM = {"scale": 4}    
def exp_mult_noise(data, snr, rate, snr_thres, rate_thres, scale_params = None):
    if scale_params is None:
        scale_params = EXP_AND_RAY_DEFAULT_SCALE_PARAM 
    '''Apply multiplicative exponential noise with a random scale value onto raw waveform data; scale_params = {scale: None}'''
    data_noisy = np.empty(data.shape)
    if np.random.uniform(0, rate_thres) < rate and snr >= snr_thres: 
        data_noisy = np.empty((data.shape))
        data_noisy[:, 0] = data[:,0] * (1 + np.random.exponential(scale_params["scale"], data.shape[0]))
        data_noisy[:, 1] = data[:,1] * (1 + np.random.exponential(scale_params["scale"], data.shape[0]))
        data_noisy[:, 2] = data[:,2] * (1 + np.random.exponential(scale_params["scale"], data.shape[0])) 
    else:
        data_noisy = data
    return data_noisy   

def ray_mult_noise(data, snr, rate, snr_thres, rate_thres, scale_params = None):
    '''Apply multiplicative Rayleigh noise with a random scale value onto raw waveform data; scale_params = {scale: None}'''
    if scale_params is None:
        scale_params = EXP_AND_RAY_DEFAULT_SCALE_PARAM 
    data_noisy = np.empty(data.shape)
    if np.random.uniform(0, rate_thres) < rate and snr >= snr_thres: 
        data_noisy = np.empty((data.shape))
        data_noisy[:, 0] = data[:,0] * (1 + np.random.rayleigh(scale_params["scale"], data.shape[0]))
        data_noisy[:, 1] = data[:,1] * (1 + np.random.rayleigh(scale_params["scale"], data.shape[0]))
        data_noisy[:, 2] = data[:,2] * (1 + np.random.rayleigh(scale_params["scale"], data.shape[0])) 
    else:
        data_noisy = data
    return data_noisy   

def exp_add_noise(data, snr, rate, snr_thres, rate_thres, scale_params = None):
    if scale_params is None:
        scale_params = EXP_AND_RAY_DEFAULT_SCALE_PARAM
    '''Apply additive Gaussian noise with a random scale variable onto raw waveform data; scale_params = {scale: None}'''
    data_noisy = np.empty(data.shape)
    if np.random.uniform(0, rate_thres) < rate and snr >= snr_thres: 
        data_noisy = np.empty((data.shape))
        signs = np.random.choice([-1,1],data.shape[0])
        data_noisy[:, 0] = data[:, 0] + (signs*np.random.exponential(scale_params["scale"], data.shape[0]))
        data_noisy[:, 1] = data[:, 1] + (signs*np.random.exponential(scale_params["scale"], data.shape[0]))
        data_noisy[:, 2] = data[:, 2] + (signs*np.random.exponential(scale_params["scale"], data.shape[0])) 
    else:
        data_noisy = data
    return data_noisy   
