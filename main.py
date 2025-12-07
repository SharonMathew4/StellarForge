"""
StellarForge - Cosmic Simulation Application
Main entry point for the application with comprehensive error handling.
"""

import sys
import uuid
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer

from core.exceptions import StellarForgeException, UIError
from core.error_logger import get_error_logger, ErrorSeverity
from gui import MainWindow
from gui.splash_screen import show_splash_screen


def setup_error_handling(app: QApplication):
    """
    Setup global error handling for the application.
    
    Args:
        app: Qt application instance
    """
    error_logger = get_error_logger()
    session_id = str(uuid.uuid4())
    error_logger.set_session_id(session_id)
    
    # Register error callback to show dialog for critical errors
    def on_error_callback(record):
        if record.severity in ["ERROR", "CRITICAL", "FATAL"]:
            try:
                QMessageBox.critical(
                    None,
                    "Application Error",
                    f"An error occurred:\n\n{record.message}\n\n"
                    f"Error Code: {record.error_code}\n"
                    f"Check logs for more details."
                )
            except Exception:
                pass
    
    error_logger.register_error_callback(on_error_callback)
    
    # Setup Qt error handler
    def qt_exception_handler(exc_type, exc_value, exc_traceback):
        error_logger.python_logger.critical(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
        sys.exit(1)
    
    sys.excepthook = qt_exception_handler


def main():
    """Main application entry point with error handling."""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='StellarForge - Cosmic Simulation Application')
    parser.add_argument('--engine', choices=['mock', 'cpp'], default='mock',
                       help='Physics engine to use (default: mock)')
    parser.add_argument('--backend', choices=['single', 'openmp', 'cuda', 'opengl'], 
                       default='openmp',
                       help='C++ engine backend (default: openmp)')
    args = parser.parse_args()
    
    use_cpp = (args.engine == 'cpp')
    
    try:
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("StellarForge")
        app.setOrganizationName("StellarForge")
        app.setApplicationVersion("1.0.0")
        
        # Setup error handling
        setup_error_handling(app)
        error_logger = get_error_logger()
        error_logger.log_error(
            f"Application started (engine: {args.engine}, backend: {args.backend})",
            component="MAIN",
            severity=ErrorSeverity.INFO
        )
        
        try:
            # Show splash screen
            splash = show_splash_screen()
            splash.showMessage("Initializing StellarForge...")
            app.processEvents()
            
            # Create window with error handling
            window = None
            
            def create_window():
                nonlocal window
                try:
                    splash.showMessage("Loading UI components...")
                    app.processEvents()
                    
                    # Create main window (hidden initially)
                    window = MainWindow(use_cpp_engine=use_cpp, backend=args.backend)
                    
                    splash.showMessage("Initializing simulation engine...")
                    app.processEvents()
                    
                    # Finish loading
                    splash.finish_loading()
                    app.processEvents()
                    
                    # Show window and close splash
                    window.show()
                    splash.finish(window)
                    
                    error_logger.log_error(
                        "Main window created successfully",
                        component="MAIN",
                        severity=ErrorSeverity.INFO
                    )
                
                except UIError as ui_error:
                    error_logger.log_exception(
                        ui_error,
                        component="MAIN_WINDOW_CREATION",
                        severity=ErrorSeverity.CRITICAL
                    )
                    splash.hide()
                    QMessageBox.critical(
                        None,
                        "UI Initialization Failed",
                        f"Failed to initialize main window:\n{ui_error.message}\n\n"
                        f"Please check the logs for more details."
                    )
                    sys.exit(1)
                
                except Exception as e:
                    error_logger.log_exception(
                        e,
                        component="MAIN_WINDOW_CREATION",
                        severity=ErrorSeverity.CRITICAL,
                        context={'step': 'window_creation'}
                    )
                    splash.hide()
                    QMessageBox.critical(
                        None,
                        "Fatal Error",
                        f"An unexpected error occurred during initialization:\n{str(e)}\n\n"
                        f"Please check the logs for more details."
                    )
                    sys.exit(1)
            
            # Create window immediately (not delayed)
            create_window()
            
            # Run application event loop
            exit_code = app.exec()
            
            error_logger.log_error(
                "Application closed normally",
                component="MAIN",
                severity=ErrorSeverity.INFO
            )
            
            # Export error log on exit
            error_logger.export_errors(Path("logs/final_error_report.json"))
            
            sys.exit(exit_code)
        
        except Exception as e:
            error_logger.log_exception(
                e,
                component="APPLICATION_SETUP",
                severity=ErrorSeverity.FATAL
            )
            QMessageBox.critical(
                None,
                "Fatal Application Error",
                f"Failed to setup application:\n{str(e)}\n\n"
                f"Logs have been saved."
            )
            sys.exit(1)
    
    except ImportError as import_error:
        print(f"Import Error: Failed to import required module: {import_error}")
        print("Please ensure all dependencies are installed.")
        sys.exit(1)
    
    except Exception as e:
        print(f"Critical Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
