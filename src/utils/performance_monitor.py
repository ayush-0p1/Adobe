# src/utils/performance_monitor.py
import time
import psutil
import logging
from contextlib import contextmanager

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        
    @contextmanager
    def measure_execution(self, operation_name: str):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            yield
        finally:
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            self.metrics[operation_name] = {
                'execution_time': end_time - start_time,
                'memory_usage': end_memory - start_memory,
                'timestamp': time.time()
            }
            
    def check_constraints(self, max_time: float, max_memory: float):
        """Check if performance meets hackathon constraints"""
        for operation, metrics in self.metrics.items():
            if metrics['execution_time'] > max_time:
                logging.warning(f"{operation} exceeded time limit: {metrics['execution_time']:.2f}s")
            if metrics['memory_usage'] > max_memory:
                logging.warning(f"{operation} exceeded memory limit: {metrics['memory_usage']:.2f}MB")

