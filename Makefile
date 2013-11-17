all:
	$(MAKE) -C rider-control-id/abstract
	$(MAKE) -C rider-control-id/poster
	$(MAKE) -C whipple-system-id/paper
	$(MAKE) -C whipple-system-id/abstract
	$(MAKE) -C steer-torque/paper
	$(MAKE) -C steer-torque/abstract
