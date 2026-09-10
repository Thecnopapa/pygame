
# VARS
export PYGAME_DETECT_AVX2=1 


assets(){
	cd "${PROJECT_PATH}/jueguito-art"
}

game(){
	cd "${PROJECT_PATH}/games/jueguitoV1"
}

play(){
	game
	python main.py
}


debug(){
	swarm
	python main.py --debug
}

	

