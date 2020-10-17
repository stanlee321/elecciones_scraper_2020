.PHOY: up
.PHOY: down

up:
	docker-compose stop
	docker-compose down
	#docker volume rm scraper-service
	docker volume create --name=scraper-service
	docker-compose -f docker-compose.yml up --build  -d
down:
	docker-compose stop
	docker-compose down