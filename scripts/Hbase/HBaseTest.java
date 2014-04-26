package test;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
 
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
 
public class HBaseTest {
 
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
        	File f = null;
        	f = new File("../lab1/data/Company_Profile_Stock_Profile.csv");
        	String tableName = "daily_data";
        	String[] familys = { "p", "v" };
        	
        	// create table
        	HBaseTest.creatTable(tableName, familys);
        	
        	BufferedReader br = new BufferedReader(new FileReader(f));
        	String line = null;
        	String line1 = null;
        	String[] lineInfo;
        	String[] lineInfo1;
        	br.readLine();
        	File f1 = null;
        	String dateInfo[];
        	String date = null;
        	String ticker = null;
        	HTable table = new HTable(conf, tableName);
        	// get ticker
        	while((line = br.readLine()) != null) {
        		lineInfo = line.split(",");
        		ticker = lineInfo[0];
        		f1 = new File("../lab1/data/PriceData/"+ticker+".csv");
        		BufferedReader br1 = new BufferedReader(new FileReader(f1));
        		br1.readLine();
        		// go through ticker prices
        		while ((line1 = br1.readLine()) != null) {
        			lineInfo1 = line1.split(",");
        			dateInfo = lineInfo1[0].split("-");
        			date = dateInfo[0]+dateInfo[1]+dateInfo[2];
	        		HBaseTest.addRecord(table, tableName, ticker+"_"+date, "p", "open", lineInfo1[1]);
	        		HBaseTest.addRecord(table, tableName, ticker+"_"+date, "p", "close", lineInfo1[4]);
	        		HBaseTest.addRecord(table, tableName, ticker+"_"+date, "p", "high", lineInfo1[2]);
	        		HBaseTest.addRecord(table, tableName, ticker+"_"+date, "p", "low", lineInfo1[3]);
	        		HBaseTest.addRecord(table, tableName, ticker+"_"+date, "v", "volume", lineInfo1[5]);
        		}
        	}
        	HBaseTest.getAllRecord(tableName);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}