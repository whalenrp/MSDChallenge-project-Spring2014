src_dir = MSDMain
lib_dir = lib
main = MSDMain.Main
classpath = .:$(lib_dir)/*:../hbase-0.94.17/lib/*:../Programs/hbase-0.94.17/*

all:
	javac -classpath $(classpath) Main.java
	
clean:
	rm Main.class
	
run:
	java -cp . Main