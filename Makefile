PROG=fpaste
BINDIR=/usr/bin
MANDIR=/usr/share/man

#ifeq ($(UID), 0)
#BINDIR=/usr/bin
#else
#BINDIR=~/bin
#endif

fpaste: install


install:
	install -p -m0755 $(PROG) $(BINDIR)
	install -d $(MANDIR)/man1
	install -p -m 644 docs/man/en/$(PROG).1 $(MANDIR)/man1/

uninstall:
	rm -f $(BINDIR)/$(PROG)
	rm -f $(MANDIR)/man1/$(PROG).1
