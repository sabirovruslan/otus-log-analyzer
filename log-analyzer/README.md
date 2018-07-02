## Анализатор логов

Для запуска через makefile требуется установленный docker

Команды make необходимо выполнять из корневой директории проекта

### Запуск Unit тестов

```
make unit-test
```

### Запуск анализатора (ООП)

```
make log-analyzer
```

### Запуск анализатора с переопределенным конфигом (ООП)

```
make log-analyzer-config
```

### Запуск анализатора (Процедурный стиль)

```
make analyze
```

### Запуск анализатора с переопределенным конфигом (Процедурный стиль)

```
make analyze-config
```

### Ручной запуск анализатора

```
python3 log_analyzer.py
```

или 

```
python log_analyzer.py --config ./config.cfg
```