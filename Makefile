SIZES := 16 24 32 48 64 128 256
SVG_DIR := icons/svg
PNG_DIR := icons/png
MSDF_DIR := icons/msdf
MSDF_SIZE := 64
MSDF_RANGE := 4

SVGS := $(wildcard $(SVG_DIR)/*.svg)
PNG_TARGETS := $(foreach size,$(SIZES),$(patsubst $(SVG_DIR)/%.svg,$(PNG_DIR)/$(size)x$(size)/%.png,$(SVGS)))
MSDF_TARGETS := $(patsubst $(SVG_DIR)/%.svg,$(MSDF_DIR)/%.png,$(SVGS))

all: png msdf

png: $(PNG_TARGETS)

msdf: $(MSDF_TARGETS)

define size_rule
$(PNG_DIR)/$(1)x$(1)/%.png: $(SVG_DIR)/%.svg | $(PNG_DIR)/$(1)x$(1)
	rsvg-convert -w $(1) -h $(1) $$< -o $$@

$(PNG_DIR)/$(1)x$(1):
	mkdir -p $$@
endef

$(foreach size,$(SIZES),$(eval $(call size_rule,$(size))))

$(MSDF_DIR)/%.png: $(SVG_DIR)/%.svg | $(MSDF_DIR)
	msdfgen msdf -svg $< -o $@ -size $(MSDF_SIZE) $(MSDF_SIZE) -pxrange $(MSDF_RANGE)

$(MSDF_DIR):
	mkdir -p $@

clean:
	rm -rf $(PNG_DIR) $(MSDF_DIR)

.PHONY: all png msdf clean
