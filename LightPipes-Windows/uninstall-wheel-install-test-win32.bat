call delete_build_dir.bat
call delete_dist_dir.bat
call build-win32.bat
call pip-uninstall-win32.bat
call makewheel-win32.bat
call pip-install-win32.bat
call test-win32.bat

