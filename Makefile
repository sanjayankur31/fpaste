PROG=fpaste
DESTDIR=
PREFIX=/usr
BINDIR=$(PREFIX)/bin
MANDIR=$(PREFIX)/share/man

#ifeq ($(UID), 0)
#BINDIR=/usr/bin
#else
#BINDIR=~/bin
#endif

fpaste: install


install:
	install -d $(DESTDIR)$(BINDIR)
	install -p -m0755 $(PROG) $(DESTDIR)$(BINDIR)
	install -d $(DESTDIR)$(MANDIR)/man1
	install -p -m 644 docs/man/en/$(PROG).1 $(DESTDIR)$(MANDIR)/man1/

uninstall:
	rm -f $(DESTDIR)$(BINDIR)/$(PROG)
	rm -f $(DESTDIR)$(MANDIR)/man1/$(PROG).1

manual:
	help2man -N --section=1 ./fpaste -o fpaste.1
	cat ./docs/man/en/common.h2m >> fpaste.1
	mv fpaste.1 ./docs/man/en/fpaste.1
