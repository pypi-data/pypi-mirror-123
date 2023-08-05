BUILD_DIR_NAME ?= build
BUILD_DIR      ?= $($(PROJ)_DIR)/$(BUILD_DIR_NAME)
$(BUILD_DIR):
	@mkdir -p $@
	@touch $@

#
# Get the last element in a space-delimited list.
# https://ftp.gnu.org/old-gnu/Manuals/make/html_node/make_17.html
#
# 1: a space-delimited list of tokens
#
get_last_word = $(word $(words $(1)), $(1))

#
# Get the full path to the currently loaded makefile. 
#
get_current_makefile = $(call get_last_word,$(MAKEFILE_LIST))

#
# Strip the name filename from a makefile path.
# https://www.gnu.org/software/make/manual/html_node/Text-Functions.html
#
# 1: makefile path
# 2: makefile name
#
makefile_to_dir = $(patsubst %/$(2),%,$(1))

#
# Allows any makefile to include other makefiles with relative paths only.
#
MK_CFG_NAME ?= conf.mk
get_current_makefile_dir = $(call makefile_to_dir,$(call get_current_makefile),$(MK_CFG_NAME))

MK_SRC_DIR  := $(call get_current_makefile_dir)
MK_PY_DIR   := $(MK_SRC_DIR)/..
MK_DATA_DIR := $(MK_SRC_DIR)/data
include $(MK_SRC_DIR)/functions.mk
include $(MK_SRC_DIR)/venv.mk
include $(MK_SRC_DIR)/python.mk
include $(MK_SRC_DIR)/pypi.mk
include $(MK_SRC_DIR)/vmklib.mk
include $(MK_SRC_DIR)/datazen.mk
include $(MK_SRC_DIR)/grip.mk
