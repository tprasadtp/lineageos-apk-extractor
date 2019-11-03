NAME := lineageos-apk-extractor
include base.mk

.PHONY: clean
clean: ## Clean
	@echo -e "\033[92m+ $@ \033[0m"
	@rm -rf __pycache__/*
	@rm -rf releases/
	@rm -rf metadata/
	@rm -rf build/

.PHONY: protoc
protoc: ## compile protoc
	@echo -e "\033[92m+ $@ \033[0m"
	@echo -e "\033[34m Generating protobuf file...\033[0m"
	@protoc -I=vendor --python_out=vendor vendor/update-metadata.proto
