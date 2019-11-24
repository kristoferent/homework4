Запуск производится в три стадии:
1) Запустить сервер CoreNLP: перейти в папку stanford-corenlp-full-2018-10-05 и ввести в терминал:
java -Xmx2g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 50000
2) Открыть другой терминал (сервер) и ввести:
python3 task1-s.py (python3 task2-s.py)
3) Открыть еще один терминал (клиента) и ввести:
python3 task1-c.py (python3 task2-c.py)
И после этого ввести команду ENTI или STAT
