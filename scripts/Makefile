src_dir = MSDMain
lib_dir = lib
main = MSDMain.Main
classpath = .:$(lib_dir)/*:hbase-0.94.18/lib/*:hbase-0.94.18/*

all:
	javac -classpath $(classpath) Main.java
	
clean:
	rm Main.class
	
run:
	java -cp $(classpath) Main
