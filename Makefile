SHELL = /bin/sh

#
# import environment variables
#
ifneq (,$(wildcard ./.env))
	include .env
	export
endif

#
# define CLI prefix for commands
#
BLUE_ = \033[34m
CYAN_ = \033[36m
GRAY_ = \033[90m
BOLD_ = \033[1m
_ENDF = \033[0m
define prompt
	@echo "$(CYAN_)make:$@$(GRAY_)$$$(_ENDF) \c"
endef
define header
	@echo ""
	@echo "$(BLUE_)$(BOLD_)************************************************************$(_ENDF)"
	@echo "$(BLUE_):: $(CYAN_)make.target = $(BOLD_)$@$(_ENDF)"
	@echo "$(BLUE_)$(BOLD_)************************************************************$(_ENDF)"
endef

#
# common values
#
sam-dir = .aws-sam
src-pip-reqts = src/requirements.txt
src-py-files = src/*.py
venv-dir = .venv

#
# configure goals
#
default: lint unittest dist
.PHONY: .gitignore mostlyclean clean destroy init deplock diagrams lint unittest dist deploy e2etest

#
# create .gitignore file
#
.gitignore:
	$(call header)
	$(call prompt) 
	curl https://www.toptal.com/developers/gitignore/api/linux,osx,pycharm,python,virtualenv,visualstudiocode,windows > $@
	$(call prompt) 
	cat .utils/gitignore.ext >> $@

#
# remove generated files from project
#
mostlyclean:
	$(call header)
	$(call prompt)
	rm -rf $(sam-dir)
	$(call prompt)
	rm -rf .coverage
	$(call prompt)
	rm -rf **/.pytest_cache
	$(call prompt)
	rm -rf **/__pycache__	
clean: | mostlyclean
	$(call header)
	$(call prompt)
	rm -rf $(venv-dir)
	$(call prompt)
	rm -f $(src-pip-reqts)
destroy:
	$(call header)
	$(call prompt)
	aws cloudformation delete-stack \
		--stack-name "${STACK_NAME}" | jq -rc .

#
# Poetry initialization rules
#
$(venv-dir): poetry.lock
	$(call header)
	$(call prompt)
	poetry install
	$(call prompt)
	touch $@
$(src-pip-reqts): pyproject.toml poetry.lock
	$(call header)
	$(call prompt)
	poetry export -f requirements.txt > $@

#
# initialization rules
#
init: $(venv-dir) $(src-pip-reqts)
deplock:
	$(call header)
	$(call prompt)
	poetry lock
	$(call prompt)
	touch $@

#
# diagram generation rule
#
diagrams: | init
	$(call header)
	$(call prompt)
	poetry run python3 docs/overview_diagram.py

#
# project linting rule
# 	* find pyilnt errors (exit non-zero if found)
# 	* list pylint warnings (exit zero always)
#	* find flake8 errors (exit non-zero if found)
#   * validate Python docstring conventions
#
lint: | init
	$(call header)
	$(call prompt)
	poetry run pylint --errors-only src docs tests
	$(call prompt)
	poetry run pylint --exit-zero src docs tests
	$(call prompt)
	poetry run flake8 --benchmark --count src docs tests
	$(call prompt)
	poetry run pydocstyle --match='.*\.py' --count src docs tests

#
# project unit testing rule
#
unittest: | init
	$(call header)
	$(call prompt)
	poetry run pytest --cov=src/ tests/unit

#
# project building rule
#   * validate the SAM template
#   * build the local build artifacts
#   * package the artifacts and deliver to S3 bucket
#
$(sam-dir): $(venv-dir) template.yaml $(src-py-files)
	$(call header)
	$(call prompt)
	poetry run sam validate
	$(call prompt)
	poetry run sam build
	$(call prompt)
	touch $@
dist: $(sam-dir)

#
# project integration testing rule
#
inttest: | init dist
	$(call header)
	$(call prompt)
	poetry run sam local invoke minecraft-local-get-servers \
		--event tests/integration/get-servers.json \
		--parameter-overrides "\
			ParameterKey=Environment,ParameterValue=local \
			ParameterKey=FunctionRole,ParameterValue=${FUNCTION_ROLE_ARN} \
		" \
		| jq -r '.body'
	poetry run sam local invoke minecraft-local-get-server \
		--event tests/integration/get-servers-dream.json \
		--parameter-overrides "\
			ParameterKey=Environment,ParameterValue=local \
			ParameterKey=FunctionRole,ParameterValue=${FUNCTION_ROLE_ARN} \
		" \
		| jq -r '.body'
	poetry run sam local invoke minecraft-local-get-users \
		--event tests/integration/get-users.json \
		--parameter-overrides "\
			ParameterKey=Environment,ParameterValue=local \
			ParameterKey=FunctionRole,ParameterValue=${FUNCTION_ROLE_ARN} \
		" \
		| jq -r '.body'
		

#
# deploy the application to AWS
#
deploy: | init dist
	$(call header)
	$(call prompt)
	poetry run sam deploy \
		--stack-name "${STACK_NAME}" \
		--s3-bucket "${S3_DEPLOYMENT_BUCKET}" \
		--s3-prefix "${STACK_NAME}" \
		--capabilities CAPABILITY_NAMED_IAM \
		--role-arn "${CLOUDFORMATION_ROLE_ARN}" \
		--no-fail-on-empty-changeset \
		--parameter-overrides "\
			ParameterKey=Environment,ParameterValue=${ENVIRONMENT} \
			ParameterKey=EventBridgeRole,ParameterValue=${EVENTBRIDGE_ROLE_ARN} \
			ParameterKey=FunctionRole,ParameterValue=${FUNCTION_ROLE_ARN} \
			ParameterKey=StateMachineRole,ParameterValue=${STATEMACHINE_ROLE_ARN} \
			ParameterKey=ApiDomainName,ParameterValue=${API_DOMAIN_NAME} \
			ParameterKey=HostedZoneId,ParameterValue=${HOSTED_ZONE_ID} \
			ParameterKey=CertificateArn,ParameterValue=${CERTIFICATE_ARN} \
		"

#
# project end-to-end testing rule
#
e2etest: | init
	$(call header)
	$(call prompt)
	poetry run pytest tests/e2e
