algo=monte_carlo
scale=1.0

run:
	$(PWD)/miniconda_pygame/bin/python ./game.py --algo $(algo) --scale $(scale)

run_no_gui:
	$(PWD)/miniconda_pygame/bin/python ./game.py --algo $(algo) --daemon

install: | install_conda check_if_need_to_apply_ubuntu_22_04_fix_for_pygame

install_conda: download_miniconda
	@chmod 755 ./miniconda.sh
	@./miniconda.sh -b -p $(PWD)/miniconda_pygame -f && $(PWD)/miniconda_pygame/bin/conda config --set auto_activate_base false
	@PYTHONPATH=$(PWD)/miniconda_pygame/bin/python;$(PWD)/miniconda_pygame/bin/python -m pip install pygame numpy pydantic scipy sympy pyyaml pytest
	@rm -rf ./miniconda.sh
	

download_miniconda:
	@bash -c "if [[ `uname` == 'Darwin' ]]; then make download_miniconda_macos; else make download_miniconda_linux; fi"
	
check_if_need_to_apply_ubuntu_22_04_fix_for_pygame:
	@bash -c "if [[ `grep -e jammy /etc/os-release | wc -l` == 1 ]]; then make apply_ubuntu_22_04_patch; fi"

apply_ubuntu_22_04_patch:
	@cd $(PWD)/miniconda_pygame/lib &&\
	mkdir backup &&\
	mv libstd* ./backup/ &&\
	LAST_FILE=`ls -1 $(PWD)/miniconda_pygame/lib/backup | tail -n 1` && \
	cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 ./ &&\
	ln -s libstdc++.so.6 libstdc++.so
    
download_miniconda_linux:
	@curl https://repo.anaconda.com/miniconda/Miniconda3-py38_4.12.0-Linux-x86_64.sh -o miniconda.sh
	
clean:
	@rm -rf ./miniconda_pygame
	@rm -rf ./miniconda.sh

download_miniconda_macos:
	@bash -c "if [[ `uname -m` == 'x86_64' ]]; then make download_miniconda_macos_x86_64; else make download_miniconda_macos_m1; fi"

download_miniconda_macos_x86_64:
	@curl https://repo.anaconda.com/miniconda/Miniconda3-py38_4.12.0-MacOSX-x86_64.sh -o miniconda.sh

download_miniconda_macos_m1:
	@curl https://repo.anaconda.com/miniconda/Miniconda3-py38_4.12.0-MacOSX-arm64.sh -o miniconda.sh

list_algos:
	@find ./algos -maxdepth 1 -type f -name '*.py' | sed "s/...$$//" | sed "s/........//"

