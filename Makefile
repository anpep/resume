LOCALES := $(shell ls "locales")
TEMPLATE := tex/template.tex

all: $(patsubst %,out/resume_%.pdf,${LOCALES})

define TARGET_MACRO
out/resume_${1}.pdf: out/template_${1}.tex
	-@env TEXINPUTS=".:tex:" pdflatex -interaction=nonstopmode -output-directory=out -jobname=resume_${1} out/template_${1}.tex

out/template_${1}.tex: ${TEMPLATE}
	@mkdir -p out/
	@python3 tools/template_processor.py locales/${1}/locale.yaml ${TEMPLATE} -o out/template_${1}.tex
endef

$(foreach locale, ${LOCALES}, $(eval $(call TARGET_MACRO,${locale})))

clean:
	rm -rf out/

.PHONY: clean all
