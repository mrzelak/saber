test:
	@python main.py

log:
	@vim -O log.fail log.success

enc:
	@python cipher.py

dec:
	@python decipher.py

key:
	@python keygen.py

ed:
	@vim -p main.py decipher.py cipher.py keygen.py utils.py tests.py params.py zq.py

.PHONY: test ed log
