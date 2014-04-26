package test;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.List;
import java.lang.Math;
 
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;
import org.apache.hadoop.hbase.KeyValue;
import org.apache.hadoop.hbase.MasterNotRunningException;
import org.apache.hadoop.hbase.ZooKeeperConnectionException;
import org.apache.hadoop.hbase.client.Delete;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.HBaseAdmin;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.util.Bytes;
import org.joda.time.DateTime;
import org.joda.time.Weeks;
 
public class HBaseQuery {
 
    private static Configuration conf = null;
    /**
     * Initialization
     */
    static {
        conf = HBaseConfiguration.create();
    }
 
    /**
     * Create a table
     */
    public static void creatTable(String tableName, String[] familys)
            throws Exception {
        HBaseAdmin admin = new HBaseAdmin(conf);
        if (admin.tableExists(tableName)) {
            System.out.println("table already exists!");
        } else {
            HTableDescriptor tableDesc = new HTableDescriptor(tableName);
            for (int i = 0; i < familys.length; i++) {
                tableDesc.addFamily(new HColumnDescriptor(familys[i]));
            }
            admin.createTable(tableDesc);
            System.out.println("create table " + tableName + " ok.");
        }
    }
 
    /**
     * Delete a table
     */
    public static void deleteTable(String tableName) throws Exception {
        try {
            HBaseAdmin admin = new HBaseAdmin(conf);
            admin.disableTable(tableName);
            admin.deleteTable(tableName);
            System.out.println("delete table " + tableName + " ok.");
        } catch (MasterNotRunningException e) {
            e.printStackTrace();
        } catch (ZooKeeperConnectionException e) {
            e.printStackTrace();
        }
    }
 
    /**
     * Put (or insert) a row
     */
    public static void addRecord(HTable table, String tableName, String rowKey,
            String family, String qualifier, String value) throws Exception {
        try {
            //HTable table = new HTable(conf, tableName);
            Put put = new Put(Bytes.toBytes(rowKey));
            put.add(Bytes.toBytes(family), Bytes.toBytes(qualifier), Bytes
                    .toBytes(value));
            table.put(put);
            //System.out.println("insert recorded " + rowKey + " to table "
            //        + tableName + " ok.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
 
    /**
     * Delete a row
     */
    public static void delRecord(String tableName, String rowKey)
            throws IOException {
        HTable table = new HTable(conf, tableName);
        List<Delete> list = new ArrayList<Delete>();
        Delete del = new Delete(rowKey.getBytes());
        list.add(del);
        table.delete(list);
        System.out.println("del recored " + rowKey + " ok.");
    }
 
    /**
     * Get a row
     */
    public static void getOneRecord (String tableName, String rowKey) throws IOException{
        HTable table = new HTable(conf, tableName);
        Get get = new Get(rowKey.getBytes());
        Result rs = table.get(get);
        for(KeyValue kv : rs.raw()){
            System.out.print(new String(kv.getRow()) + " " );
            System.out.print(new String(kv.getFamily()) + ":" );
            System.out.print(new String(kv.getQualifier()) + " " );
            System.out.print(kv.getTimestamp() + " " );
            System.out.println(new String(kv.getValue()));
        }
    }
    /**
     * Scan (or list) a table
     */
    public static void getAllRecord (String tableName) {
        try{
             HTable table = new HTable(conf, tableName);
             Scan s = new Scan();
             ResultScanner ss = table.getScanner(s);
             for(Result r:ss){
                 for(KeyValue kv : r.raw()){
                    System.out.print(new String(kv.getRow()) + " ");
                    System.out.print(new String(kv.getFamily()) + ":");
                    System.out.print(new String(kv.getQualifier()) + " ");
                    System.out.print(kv.getTimestamp() + " ");
                    System.out.println(new String(kv.getValue()));
                 }
             }
        } catch (IOException e){
            e.printStackTrace();
        }
    }
 
    public static void main(String[] agrs) {
        try {
/*            String tablename = "scores";
            String[] familys = { "grade", "course" };
            HBaseTest.creatTable(tablename, familys);
 
            // add record zkb
            HBaseTest.addRecord(tablename, "zkb", "grade", "", "5");
            HBaseTest.addRecord(tablename, "zkb", "course", "", "90");
            HBaseTest.addRecord(tablename, "zkb", "course", "math", "97");
            HBaseTest.addRecord(tablename, "zkb", "course", "art", "87");
            // add record baoniu
            HBaseTest.addRecord(tablename, "baoniu", "grade", "", "4");
            HBaseTest.addRecord(tablename, "baoniu", "course", "math", "89");
 
            System.out.println("===========get one record========");
            HBaseTest.getOneRecord(tablename, "zkb");
 
            System.out.println("===========show all record========");
            HBaseTest.getAllRecord(tablename);
 
            System.out.println("===========del one record========");
            HBaseTest.delRecord(tablename, "baoniu");
            HBaseTest.getAllRecord(tablename);
 
            System.out.println("===========show all record========");
            HBaseTest.getAllRecord(tablename);*/
        	/*String tableName = "daily_data";
            HTable table = new HTable(conf, tableName);
            String stockname = "AAPL";
            String stockstart = stockname + "_" + "20100101";
            String stockend = stockname + "_" + "20110101";
            int days = 0;
            int weeks = 0;
            double curWeek = 0;
            Scan s = new Scan(Bytes.toBytes(stockstart), Bytes.toBytes(stockend));
            ResultScanner ss = table.getScanner(s);
            double average = 0;
            for(Result r:ss){
                for(KeyValue kv : r.raw()){
                	String qualifier = new String(kv.getQualifier());
                	if (qualifier.equals("close")) {
                		curWeek += Double.parseDouble(new String(kv.getValue()));
	                	days++;
	                	if (days == 7) {
	                		average += curWeek / 7;
	                		weeks++;
	                		days = 0;
	                		curWeek = 0;
	                	}
                	}
                }
            }
            if (days != 0) {
            	average += curWeek / days;
            	weeks++;
            }
        	average = average / weeks;
        	System.out.println(average);*/
        	String tableName = "daily_data";
            HTable table = new HTable(conf, tableName);
            String stockname = "AAPL";
            String stockstart = stockname + "_" + "20100101";
            String stockend = stockname + "_" + "20110101";
            Scan s = new Scan(Bytes.toBytes(stockstart), Bytes.toBytes(stockend));
            ResultScanner ss = table.getScanner(s);
            double maximum = 0;
            double minimum = 100000000;
            for(Result r:ss){
                for(KeyValue kv : r.raw()){
                	String qualifier = new String(kv.getQualifier());
                	if (qualifier.equals("close")) {
                		maximum = Math.max(maximum, Double.parseDouble(new String(kv.getValue())));
                		minimum = Math.min(minimum, Double.parseDouble(new String(kv.getValue())));
                	}
                }
            }
            System.out.println("maximum: "+maximum);
            System.out.println("minimum: "+minimum);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}