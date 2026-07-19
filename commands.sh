
assets(){
	cd "${PROJECT_PATH}/Jueguito"
}

swarm(){
	cd "${PROJECT_PATH}/games/swarm"
}

play(){
	swarm
	python main.py
}


debug(){
	swarm
	python main.py --debug
}

	

