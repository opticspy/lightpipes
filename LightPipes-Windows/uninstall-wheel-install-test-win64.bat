call delete_build_dir.bat
call delete_dist_dir.bat
call build-win64.bat
call pip-uninstall-win64.bat
call makewheel-win64.bat
call pip-install-win64.bat
call test-win64.bat
