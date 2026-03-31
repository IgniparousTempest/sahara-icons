SIZES := 16 24 32 48 64 128 256
SVG_DIR := icons/svg
PNG_DIR := icons/png
SDF_DIR := icons/sdf
SDF_SIZE := 64
SDF_SPREAD := 8
ATLAS_PNG := icons/atlas.png
ATLAS_JSON := icons/atlas.json

SVGS := $(wildcard $(SVG_DIR)/*.svg)
PNG_TARGETS := $(foreach size,$(SIZES),$(patsubst $(SVG_DIR)/%.svg,$(PNG_DIR)/$(size)x$(size)/%.png,$(SVGS)))

all: png sdf atlas

png: $(PNG_TARGETS)

sdf: $(SVGS)
	python3 tools/gen_sdf.py $(SVG_DIR) $(SDF_DIR) $(SDF_SIZE) $(SDF_SPREAD)

atlas: sdf
	python3 tools/pack_atlas.py $(SDF_DIR) $(ATLAS_PNG) $(ATLAS_JSON)

define size_rule
$(PNG_DIR)/$(1)x$(1)/%.png: $(SVG_DIR)/%.svg | $(PNG_DIR)/$(1)x$(1)
	rsvg-convert -w $(1) -h $(1) $$< -o $$@

$(PNG_DIR)/$(1)x$(1):
	mkdir -p $$@
endef

$(foreach size,$(SIZES),$(eval $(call size_rule,$(size))))

clean:
	rm -rf $(PNG_DIR) $(SDF_DIR) $(ATLAS_PNG) $(ATLAS_JSON)

.PHONY: all png sdf atlas clean
