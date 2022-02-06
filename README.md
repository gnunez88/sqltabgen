# TabGen

This application is intended to generate values to insert in a table.

## Why this application?

Sometimes we need to test database rules with our own values or we want to
generate values for a CTF (*Capture The Flag*) challenge (this was my main
purpose).

## How to use it

Let's say we have these files:
- `id.txt`
```text
1
2
3
4
5
```

- `user.txt`
```text
john
michael
jack
laura
maria
rose
robert
```

- `pass.txt`
```text
123456
password
iloveyou
metoo
kissmerightnownaughtygirl
```

We can:
1. Just make an insert query:
```bash
python3 sqltabgen.py -t example1 id:v:69 user:v:adan pass:v:eva
```
will return:
```bash
INSERT INTO example1 (id,user,pass) values
('69','adan','eva');
```

2. We can make the `id` value not to be quoted:
```bash
python3 sqltabgen.py -t example2 id:v:69:i user:v:adan pass:v:eva
```
will return:
```bash
INSERT INTO example2 (id,user,pass) values
(69,'adan','eva');
```

3. We can generate the query using the previous dictionaries:
```bash
python3 sqltabgen.py -t example3 id:f:id.txt:i user:f:user.txt pass:f:pass.txt
```
will return:
```bash
INSERT INTO example3 (id,user,pass) values
(1,'john','123456'),
(2,'michael','password'),
(3,'jack','iloveyou'),
(4,'laura','metoo'),
(5,'maria','kissmerightnownaughtygirl');
```
**Note**: The number of entries will be as long as the shortest list.

4. We can specify the amount of entries we want:
```bash
python3 sqltabgen.py -t example4 id:f:id.txt:i user:f:user.txt pass:f:pass.txt -n3
```
will return:
```bash
INSERT INTO example4 (id,user,pass) values
(1,'john','123456'),
(2,'michael','password'),
(3,'jack','iloveyou');
```

5. We can specify to take the values from a list randomly, in this case `pass.txt`:
```bash
python3 sqltabgen.py -t example5 id:f:id.txt:i user:f:user.txt pass:fr:pass.txt -n3
```
will return:
```bash
INSERT INTO example5 (id,user,pass) values
(1,'john','metoo'),
(2,'michael','iloveyou'),
(3,'jack','kissmerightnownaughtygirl');
```

And, of course, you can both save the output to a file with `-o` and hide the output on **sSTDOUT** with `-q`.
