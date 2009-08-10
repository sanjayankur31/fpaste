PROG=fpaste
BINDIR=/usr/bin

#ifeq ($(UID), 0)
#BINDIR=/usr/bin
#else
#BINDIR=~/bin
#endif

fpaste: install


install:
	install -p -m0755 $(PROG) $(BINDIR)

uninstall:
	rm -f $(BINDIR)/$(PROG)
