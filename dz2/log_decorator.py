import datetime

# функция декоратор принимает путь к файлу в качестве аргумента и возвращает сам декоратор
def function_logger(log_file):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # сохраняем текущее время перед вызовом декорируемой функции
            start_time = datetime.now()
            # открываем указанный файл лога в режиме 'append' для добавления логов в конец файла
            with open(log_file, 'a') as log:
                # записываем инфу (имя время аргументы)
                log.write(f"Function name: {func.__name__}\n")
                log.write(f"Start time: {start_time}\n")
                log.write(f"Input arguments: Positional: {args or None}, Keyword: {kwargs or None}\n")
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    result = "Function execution failed due to an exception"
                    log.write(f"Returned value: {result}\n")
                    raise e
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                log.write(f"Returned value: {result}\n")
                log.write(f"End time: {end_time}\n")
                log.write(f"Execution time: {execution_time} seconds\n\n")
                return result
        return wrapper
    return decorator