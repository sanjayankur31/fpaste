PROG=fpaste
DESTDIR=
PREFIX=/usr
MANDIR=$(PREFIX)/share/man
SYSCONFIGDIR=/etc/

fpaste: install


install:
	install -d $(DESTDIR)$(MANDIR)/man1
	install -p -m 644 docs/man/en/$(PROG).1 $(DESTDIR)$(MANDIR)/man1/
	install -d $(DESTDIR)${SYSCONFIGDIR)}
	install -p -m 644 docs/config/${PROG}*.toml $(DESTDIR)$(SYSCONFIGDIR)/

uninstall:
	rm -f $(DESTDIR)$(SYSCONFIGDIR)/$(PROG)*.toml
	rm -f $(DESTDIR)$(MANDIR)/man1/$(PROG).1
