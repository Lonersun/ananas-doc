# Minimal makefile for Ananas documentation
#
current_root=`pwd`

doc:
	@python -mananasdoc.template $(current_root)

%: Makefile
	@python -msphinx -M html . build
        