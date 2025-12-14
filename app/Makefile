.PHONY: help install run test clean docker-build docker-run docker-stop lint format compose-up compose-down compose-logs

# Variables
APP_NAME=flask-app
DOCKER_IMAGE=$(APP_NAME)
DOCKER_TAG=latest
PORT=5000
CERT_FILE=Zscaler_Root_CA.cer
# Docker build configuration
# PARENT_DIR: Directory containing your certificate file (one level up from app/)
# APP_DIR: Relative path from PARENT_DIR to this app directory
# These assume the standard template structure: <project>/app/
# Update if your project structure differs
PARENT_DIR=..
APP_DIR=app

# Colors for output
CYAN=\033[0;36m
GREEN=\033[0;32m
YELLOW=\033[1;33m
NC=\033[0m # No Color

help: ## Show this help message
	@echo "$(CYAN)Available commands:$(NC)"
	@echo ""
	@echo "$(GREEN)Local Development:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

# ============================================================================
# Local Development
# ============================================================================

install: ## Create virtual environment and install dependencies
	@echo "$(CYAN)Setting up virtual environment...$(NC)"
	@python3 -m venv venv || true
	@echo "$(CYAN)Installing dependencies...$(NC)"
	@. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "$(GREEN)✓ Installation complete!$(NC)"

run: ## Run the Flask app locally
	@echo "$(CYAN)Starting Flask app on http://localhost:$(PORT)$(NC)"
	@. venv/bin/activate && python app.py

dev: ## Run Flask in development mode with auto-reload
	@echo "$(CYAN)Starting Flask in development mode...$(NC)"
	@. venv/bin/activate && FLASK_ENV=development flask run --host=0.0.0.0 --port=$(PORT)

shell: ## Open Python shell with app context
	@echo "$(CYAN)Opening Flask shell...$(NC)"
	@. venv/bin/activate && flask shell

# ============================================================================
# Testing
# ============================================================================

test: ## Run tests (add your test files here)
	@echo "$(CYAN)Running tests...$(NC)"
	@. venv/bin/activate && python -m pytest tests/ -v || echo "$(YELLOW)No tests found. Create tests/ directory with test files.$(NC)"

test-endpoints: ## Test API endpoints with curl
	@echo "$(CYAN)Testing API endpoints...$(NC)"
	@./test_endpoints.sh || echo "$(YELLOW)Make sure the app is running first!$(NC)"

# ============================================================================
# Docker Commands
# ============================================================================

docker-build: ## Build Docker image
	@echo "$(CYAN)Building Docker image...$(NC)"
	@cd $(PARENT_DIR) && docker build \
		--build-arg CERT_FILE=$(CERT_FILE) \
		-f $(APP_DIR)/Dockerfile \
		-t $(DOCKER_IMAGE):$(DOCKER_TAG) .
	@echo "$(GREEN)✓ Docker image built: $(DOCKER_IMAGE):$(DOCKER_TAG)$(NC)"

docker-run: ## Run Docker container
	@echo "$(CYAN)Starting Docker container...$(NC)"
	@docker run -d -p $(PORT):5000 --name $(APP_NAME) $(DOCKER_IMAGE):$(DOCKER_TAG) || \
		docker start $(APP_NAME)
	@echo "$(GREEN)✓ Container running on http://localhost:$(PORT)$(NC)"
	@echo "$(YELLOW)View logs: make docker-logs$(NC)"

docker-stop: ## Stop Docker container
	@echo "$(CYAN)Stopping Docker container...$(NC)"
	@docker stop $(APP_NAME) || true
	@echo "$(GREEN)✓ Container stopped$(NC)"

docker-rm: ## Remove Docker container
	@echo "$(CYAN)Removing Docker container...$(NC)"
	@docker rm $(APP_NAME) || true
	@echo "$(GREEN)✓ Container removed$(NC)"

docker-logs: ## View Docker container logs
	@docker logs -f $(APP_NAME)

docker-shell: ## Open shell in running Docker container
	@docker exec -it $(APP_NAME) /bin/bash

docker-rebuild: docker-stop docker-rm docker-build ## Rebuild Docker image (stops and removes old container first)

# ============================================================================
# Docker Compose Commands (for multi-container setup)
# ============================================================================

compose-up: ## Start all containers with docker-compose
	@echo "$(CYAN)Starting containers with docker-compose...$(NC)"
	@cd .. && docker-compose up -d
	@echo "$(GREEN)✓ Containers started$(NC)"
	@echo "$(YELLOW)View logs: make compose-logs$(NC)"

compose-up-build: ## Build and start all containers
	@echo "$(CYAN)Building and starting containers...$(NC)"
	@cd .. && docker-compose up --build -d
	@echo "$(GREEN)✓ Containers built and started$(NC)"

compose-down: ## Stop and remove all containers
	@echo "$(CYAN)Stopping containers...$(NC)"
	@cd .. && docker-compose down
	@echo "$(GREEN)✓ Containers stopped$(NC)"

compose-down-volumes: ## Stop containers and remove volumes (clears database)
	@echo "$(CYAN)Stopping containers and removing volumes...$(NC)"
	@cd .. && docker-compose down -v
	@echo "$(GREEN)✓ Containers stopped and volumes removed$(NC)"

compose-logs: ## View logs from all containers
	@cd .. && docker-compose logs -f

compose-logs-app: ## View logs from app container only
	@cd .. && docker-compose logs -f app

compose-logs-db: ## View logs from database container only
	@cd .. && docker-compose logs -f db

compose-ps: ## Show status of all containers
	@cd .. && docker-compose ps

compose-restart: ## Restart all containers
	@echo "$(CYAN)Restarting containers...$(NC)"
	@cd .. && docker-compose restart
	@echo "$(GREEN)✓ Containers restarted$(NC)"

compose-shell-app: ## Open shell in app container
	@cd .. && docker-compose exec app /bin/bash

compose-shell-db: ## Open PostgreSQL shell in database container
	@cd .. && docker-compose exec db psql -U $(shell cd .. && docker-compose exec -T db printenv POSTGRES_USER || echo flaskuser) -d $(shell cd .. && docker-compose exec -T db printenv POSTGRES_DB || echo flaskdb)

# ============================================================================
# Code Quality
# ============================================================================

lint: ## Run linter (add your preferred linter)
	@echo "$(CYAN)Running linter...$(NC)"
	@. venv/bin/activate && \
		python -m flake8 . --exclude=venv,__pycache__ || \
		echo "$(YELLOW)Install flake8: pip install flake8$(NC)"

format: ## Format code with black (install: pip install black)
	@echo "$(CYAN)Formatting code...$(NC)"
	@. venv/bin/activate && \
		black . --exclude=venv || \
		echo "$(YELLOW)Install black: pip install black$(NC)"

type-check: ## Run type checking with mypy (install: pip install mypy)
	@echo "$(CYAN)Running type checker...$(NC)"
	@. venv/bin/activate && \
		mypy . --ignore-missing-imports || \
		echo "$(YELLOW)Install mypy: pip install mypy$(NC)"

# ============================================================================
# AI/ML Specific Commands (examples - customize as needed)
# ============================================================================

download-models: ## Download ML models (customize for your models)
	@echo "$(CYAN)Downloading models...$(NC)"
	@mkdir -p models/data || true
	@echo "$(YELLOW)Add your model download commands here$(NC)"
	@echo "$(GREEN)Example:$(NC)"
	@echo "  wget -O models/data/model.pkl https://example.com/model.pkl"

train: ## Train ML model (customize for your training script)
	@echo "$(CYAN)Training model...$(NC)"
	@. venv/bin/activate && \
		python scripts/train.py || \
		echo "$(YELLOW)Create scripts/train.py for your training script$(NC)"

predict: ## Run prediction (customize for your prediction script)
	@echo "$(CYAN)Running prediction...$(NC)"
	@. venv/bin/activate && \
		python scripts/predict.py || \
		echo "$(YELLOW)Create scripts/predict.py for your prediction script$(NC)"

# ============================================================================
# Cleanup
# ============================================================================

clean: ## Remove Python cache files
	@echo "$(CYAN)Cleaning Python cache...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Cleaned cache files$(NC)"

clean-venv: ## Remove virtual environment
	@echo "$(CYAN)Removing virtual environment...$(NC)"
	@rm -rf venv
	@echo "$(GREEN)✓ Virtual environment removed$(NC)"

clean-docker: docker-stop docker-rm ## Stop and remove Docker container
	@echo "$(CYAN)Removing Docker image...$(NC)"
	@docker rmi $(DOCKER_IMAGE):$(DOCKER_TAG) || true
	@echo "$(GREEN)✓ Docker cleanup complete$(NC)"

clean-all: clean clean-venv clean-docker ## Clean everything (cache, venv, Docker)

# ============================================================================
# Utility Commands
# ============================================================================

requirements: ## Update requirements.txt from installed packages
	@echo "$(CYAN)Updating requirements.txt...$(NC)"
	@. venv/bin/activate && pip freeze > requirements.txt
	@echo "$(GREEN)✓ Requirements updated$(NC)"

check: ## Check if app is running
	@curl -s http://localhost:$(PORT)/api/health > /dev/null && \
		echo "$(GREEN)✓ App is running on http://localhost:$(PORT)$(NC)" || \
		echo "$(YELLOW)✗ App is not running$(NC)"

status: ## Show status of services
	@echo "$(CYAN)Service Status:$(NC)"
	@echo ""
	@echo "$(GREEN)Local:$(NC)"
	@curl -s http://localhost:$(PORT)/api/health > /dev/null && \
		echo "  ✓ Flask app running on port $(PORT)" || \
		echo "  ✗ Flask app not running"
	@echo ""
	@echo "$(GREEN)Docker:$(NC)"
	@docker ps --filter "name=$(APP_NAME)" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" || \
		echo "  ✗ Docker container not running"

# ============================================================================
# Security Checks
# ============================================================================

check-secrets: ## Check for potential secrets in code (before committing!)
	@echo "$(CYAN)Checking for potential secrets...$(NC)"
	@echo ""
	@echo "$(YELLOW)Searching for common secret patterns:$(NC)"
	@grep -r -i --include="*.py" --include="*.env*" \
		-e "password.*=" \
		-e "secret.*=" \
		-e "api_key.*=" \
		-e "token.*=" \
		-e "credential" \
		. 2>/dev/null | grep -v ".git" | grep -v "venv" | grep -v ".env.example" || \
		echo "$(GREEN)✓ No obvious secrets found in code$(NC)"
	@echo ""
	@echo "$(YELLOW)Checking for sensitive files in git:$(NC)"
	@if git ls-files 2>/dev/null | grep -E "\.(env|cer|crt|pem|key|log|db)$$"; then \
		echo "$(YELLOW)⚠ WARNING: Sensitive files found in git!$(NC)"; \
	else \
		echo "$(GREEN)✓ No sensitive files tracked$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)Checking staged files:$(NC)"
	@if git diff --cached --name-only 2>/dev/null | grep -E "\.(env|cer|crt|pem|key)$$"; then \
		echo "$(YELLOW)⚠ WARNING: Sensitive files staged for commit!$(NC)"; \
	else \
		echo "$(GREEN)✓ No sensitive files staged$(NC)"; \
	fi

pre-commit-check: check-secrets ## Run security checks before committing
	@echo ""
	@echo "$(GREEN)Pre-commit security check complete!$(NC)"

