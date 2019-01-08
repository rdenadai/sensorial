# Sensorial

## Execution

```bash
 $> gunicorn application:app --error-logfile ./error.log --access-logfile ./access.log --reload -b 0.0.0.0:8585 -w 4 -k uvicorn.workers.UvicornWorker &
```
