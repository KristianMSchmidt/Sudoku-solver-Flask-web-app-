## ----------------------------------------------------------------------
## Makefile for Fast Sudoku
##
## Used for both development and production. See targets below.
## ----------------------------------------------------------------------

help:   # Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)
	

# ---------- Development ---------- #
build:  ## Build or rebuild development docker image
	docker-compose build

develop:  ## Build or rebuild development docker image
	docker-compose up --remove-orphans


# ---------- Testing ---------- #
test: ## Execute backend test suite within a docker container
	docker-compose run app python unit_tests.py

# ---------- Production ---------- #
production_stop: ## Stop production server
	docker-compose -f docker-compose.prod.yml down --remove-orphans

production_start: ## Start production server as daemon
	docker-compose -f docker-compose.prod.yml up --build --remove-orphans -d