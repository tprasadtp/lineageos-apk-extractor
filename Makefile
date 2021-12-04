SHELL := /bin/bash
export REPO_ROOT := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

DEVICE ?=
APK_IMG ?= product

.PHONY: help
help: ## This help message
	@printf "%-20s %s\n" "Target" "Help"
	@printf "%-20s %s\n" "-----" "-----"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Clean
	@echo -e "\033[92m+ $@ \033[0m"
	rm -rf __pycache__/*
	rm -rf releases/
	rm -rf build/

.PHONY: protoc
protoc: ## Compile protocol buffers
	@echo -e "\033[92m+ $@ \033[0m"
	@protoc -I=scripts --python_out=scripts scripts/metadata.proto

.PHONY: install
install: ## Installs python dependencies
	@echo -e "\033[92m+ $@ \033[0m"
	pip3 install -r $(REPO_ROOT)/requirements.txt

.PHONY: build-payload
build-payload: ## Download and unpack (payload.bin OTA based)
	@echo -e "\033[92m+ $@ \033[0m"
	@if [[ -z $(DEVICE) ]]; then echo "DEVICE is not defined"; exit 1; fi
	$(REPO_ROOT)/scripts/fetch -d $(DEVICE) -o $(REPO_ROOT)/build/$(DEVICE)/lineageos-$(DEVICE).zip
	@echo ""
	$(REPO_ROOT)/scripts/verify -k $(REPO_ROOT)/data/lineageos.pem -z $(REPO_ROOT)/build/$(DEVICE)/lineageos-$(DEVICE).zip
	@echo ""
	$(REPO_ROOT)/scripts/unpack-payload -z $(REPO_ROOT)/build/$(DEVICE)/lineageos-$(DEVICE).zip -d $(REPO_ROOT)/build/$(DEVICE)/

.PHONY: apks
apks: ## Extract APKs (Requires root)
	@echo -e "\033[92m- Mounting Filesystem \033[0m"
	@if ! test -d /mnt/lineage-$(DEVICE)-$(APK_IMG)/; then sudo mkdir -p /mnt/lineage-$(DEVICE)-$(APK_IMG)/; fi
	sudo umount /mnt/lineage-$(DEVICE)-$(APK_IMG) || true
	sudo mount $(REPO_ROOT)/build/$(DEVICE)/$(APK_IMG).img /mnt/lineage-$(DEVICE)-$(APK_IMG)/
	@echo -e "\033[92m- Copying release assets \033[0m"
	$(REPO_ROOT)/scripts/copy-apks -k -m /mnt/lineage-$(DEVICE)-$(APK_IMG)/ -t $(REPO_ROOT)/data/transfer-$(DEVICE)-$(APK_IMG).json -d $(REPO_ROOT)/build/$(DEVICE)/apks
	@echo -e "\033[92m- UnMounting Filesystem \033[0m"
	sudo umount /mnt/lineage-$(DEVICE)-$(APK_IMG)