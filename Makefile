NAME := lineageos-apk-extractor
include base.mk

.PHONY: clean
clean: ## Clean
	@rm -rf __pycache__/*
	@rm -f releases
	@rm -f metadata
	@rm -f build
