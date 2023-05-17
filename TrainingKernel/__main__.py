from ipykernel.kernelapp import IPKernelApp
from . import TrainingKernel

IPKernelApp.launch_instance(kernel_class=TrainingKernel)
