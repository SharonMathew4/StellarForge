"""
Error diagnostics and recovery utilities for StellarForge.
Provides tools for analyzing errors, generating diagnostics reports, and recovery strategies.
"""

import json
import platform
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

from .error_logger import get_error_logger, ErrorSeverity
from .exceptions import StellarForgeException

# Optional dependency
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


class SystemDiagnostics:
    """Gather system information for diagnostics and troubleshooting."""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get system information."""
        try:
            return {
                'platform': platform.platform(),
                'python_version': platform.python_version(),
                'processor': platform.processor(),
                'machine': platform.machine(),
                'architecture': platform.architecture()[0],
                'node': platform.node(),
            }
        except Exception as e:
            get_error_logger().log_error(
                f"Failed to get system info: {e}",
                component="DIAGNOSTICS",
                severity=ErrorSeverity.WARNING
            )
            return {}
    
    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        """Get memory usage information."""
        try:
            if not HAS_PSUTIL:
                return {'note': 'psutil not installed - install for memory diagnostics'}
            
            import psutil
            memory = psutil.virtual_memory()
            process = psutil.Process()
            
            return {
                'total_memory_mb': memory.total / (1024 * 1024),
                'available_memory_mb': memory.available / (1024 * 1024),
                'used_memory_mb': memory.used / (1024 * 1024),
                'memory_percent': memory.percent,
                'process_memory_mb': process.memory_info().rss / (1024 * 1024),
                'process_memory_percent': process.memory_percent(),
            }
        except Exception as e:
            get_error_logger().log_error(
                f"Failed to get memory info: {e}",
                component="DIAGNOSTICS",
                severity=ErrorSeverity.WARNING
            )
            return {}
    
    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        """Get CPU information."""
        try:
            if not HAS_PSUTIL:
                return {'note': 'psutil not installed - install for CPU diagnostics'}
            
            import psutil
            return {
                'cpu_count_logical': psutil.cpu_count(logical=True),
                'cpu_count_physical': psutil.cpu_count(logical=False),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None,
            }
        except Exception as e:
            get_error_logger().log_error(
                f"Failed to get CPU info: {e}",
                component="DIAGNOSTICS",
                severity=ErrorSeverity.WARNING
            )
            return {}
    
    @staticmethod
    def get_full_diagnostics() -> Dict[str, Any]:
        """Get complete system diagnostics."""
        return {
            'timestamp': datetime.now().isoformat(),
            'system': SystemDiagnostics.get_system_info(),
            'memory': SystemDiagnostics.get_memory_info(),
            'cpu': SystemDiagnostics.get_cpu_info(),
        }


class ErrorDiagnosticReport:
    """Generate comprehensive diagnostic reports for errors."""
    
    def __init__(self):
        self.error_logger = get_error_logger()
    
    def generate_report(self, filepath: Optional[Path] = None) -> Dict[str, Any]:
        """
        Generate comprehensive diagnostic report.
        
        Args:
            filepath: Path to save report (optional)
            
        Returns:
            Dictionary containing diagnostic report
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_diagnostics': SystemDiagnostics.get_full_diagnostics(),
            'error_summary': self.error_logger.get_error_summary(),
            'recent_errors': [
                e.to_dict() for e in self.error_logger.get_errors(limit=20)
            ],
            'error_patterns': self._analyze_error_patterns(),
        }
        
        if filepath:
            try:
                filepath.parent.mkdir(parents=True, exist_ok=True)
                with open(filepath, 'w') as f:
                    json.dump(report, f, indent=2, default=str)
                self.error_logger.log_error(
                    f"Diagnostic report saved to {filepath}",
                    component="DIAGNOSTICS",
                    severity=ErrorSeverity.INFO
                )
            except Exception as e:
                self.error_logger.log_exception(
                    e,
                    component="DIAGNOSTICS",
                    severity=ErrorSeverity.ERROR,
                    context={'filepath': str(filepath)}
                )
        
        return report
    
    def _analyze_error_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in errors."""
        errors = self.error_logger.errors
        
        if not errors:
            return {'pattern': 'No errors'}
        
        # Find most common error codes
        error_codes = {}
        components = {}
        severities = {}
        
        for error in errors:
            error_codes[error.error_code] = error_codes.get(error.error_code, 0) + 1
            components[error.component] = components.get(error.component, 0) + 1
            severities[error.severity] = severities.get(error.severity, 0) + 1
        
        return {
            'most_common_error_codes': sorted(
                error_codes.items(), key=lambda x: x[1], reverse=True
            )[:5],
            'most_affected_components': sorted(
                components.items(), key=lambda x: x[1], reverse=True
            )[:5],
            'severity_distribution': severities,
        }


class ErrorRecoveryStrategy:
    """Strategies for recovering from specific errors."""
    
    @staticmethod
    def get_recovery_suggestion(exception: Exception) -> str:
        """
        Get suggested recovery action for an exception.
        
        Args:
            exception: The exception to analyze
            
        Returns:
            Suggested recovery message
        """
        exc_type = type(exception).__name__
        message = str(exception)
        
        suggestions = {
            'EngineInitializationError': (
                "Engine initialization failed. Try:\n"
                "1. Reduce the number of particles\n"
                "2. Check available system memory\n"
                "3. Restart the application\n"
                "4. Check logs for detailed error information"
            ),
            'RenderingError': (
                "Rendering failed. Try:\n"
                "1. Update your graphics drivers\n"
                "2. Check GPU memory usage\n"
                "3. Reduce particle count\n"
                "4. Disable advanced visual effects"
            ),
            'SimulationError': (
                "Simulation error occurred. Try:\n"
                "1. Reset the simulation\n"
                "2. Reload the last saved scenario\n"
                "3. Check system resources\n"
                "4. Pause and resume the simulation"
            ),
            'DataValidationError': (
                "Invalid data detected. Try:\n"
                "1. Clear cache and restart\n"
                "2. Reload from file\n"
                "3. Start a new simulation"
            ),
            'MemoryError': (
                "Out of memory. Try:\n"
                "1. Close other applications\n"
                "2. Reduce particle count\n"
                "3. Reduce visual quality settings\n"
                "4. Restart the application"
            ),
        }
        
        return suggestions.get(
            exc_type,
            "An error occurred. Check logs and restart the application."
        )
    
    @staticmethod
    def safe_shutdown() -> bool:
        """
        Safely shutdown the application.
        
        Returns:
            True if shutdown succeeded
        """
        try:
            error_logger = get_error_logger()
            
            # Export error logs
            log_path = Path("logs/crash_report.json")
            error_logger.export_errors(log_path)
            
            # Generate diagnostic report
            diagnostic = ErrorDiagnosticReport()
            report_path = Path("logs/diagnostic_report.json")
            diagnostic.generate_report(report_path)
            
            error_logger.log_error(
                "Application shutting down safely",
                component="SHUTDOWN",
                severity=ErrorSeverity.INFO
            )
            
            return True
        
        except Exception as e:
            print(f"Error during safe shutdown: {e}")
            return False


class ErrorContextManager:
    """Context manager for handling errors in specific operations."""
    
    def __init__(self, operation_name: str, component: str):
        """
        Initialize context manager.
        
        Args:
            operation_name: Name of the operation
            component: Component performing the operation
        """
        self.operation_name = operation_name
        self.component = component
        self.error_logger = get_error_logger()
        self.start_time = None
    
    def __enter__(self):
        """Enter context."""
        self.start_time = datetime.now()
        self.error_logger.log_error(
            f"Starting operation: {self.operation_name}",
            component=self.component,
            severity=ErrorSeverity.DEBUG
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context with error handling."""
        now = datetime.now()
        duration = (now - self.start_time).total_seconds() if self.start_time else 0.0
        
        if exc_type is None:
            self.error_logger.log_error(
                f"Operation completed: {self.operation_name} ({duration:.2f}s)",
                component=self.component,
                severity=ErrorSeverity.DEBUG
            )
            return False
        else:
            # Error occurred
            severity = ErrorSeverity.CRITICAL if issubclass(exc_type, Exception) else ErrorSeverity.ERROR
            
            self.error_logger.log_error(
                f"Operation failed: {self.operation_name} ({duration:.2f}s)",
                component=self.component,
                severity=severity,
                context={
                    'error_type': exc_type.__name__,
                    'error_message': str(exc_val),
                    'duration_seconds': duration
                }
            )
            
            # Print recovery suggestion if available
            recovery = ErrorRecoveryStrategy.get_recovery_suggestion(exc_val)
            self.error_logger.python_logger.error(f"\nRecovery suggestion:\n{recovery}")
            
            # Return False to propagate the exception
            return False


def setup_error_handlers():
    """Setup global error handlers for the application."""
    error_logger = get_error_logger()
    
    # Register callback to generate diagnostic reports on critical errors
    def on_critical_error(record):
        if record.severity in ["CRITICAL", "FATAL"]:
            try:
                diagnostic = ErrorDiagnosticReport()
                report_path = Path(f"logs/critical_error_{record.timestamp.replace(':', '-')}.json")
                diagnostic.generate_report(report_path)
            except Exception as e:
                error_logger.python_logger.error(f"Failed to generate diagnostic report: {e}")
    
    error_logger.register_error_callback(on_critical_error)
