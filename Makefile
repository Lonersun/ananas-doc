current_root=`pwd`
docs:
	vim template/_version/note
	#sh make_docs.sh


install:
	test -x 'bin/ananas-doc' || chmod +x bin/ananas-doc
