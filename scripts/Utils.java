// pulled from Lab 2
package src;
import org.apache.hadoop.hbase.filter.InclusiveStopFilter;
import org.apache.hadoop.hbase.filter.PrefixFilter;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.util.Bytes;
import java.security.NoSuchAlgorithmException;
import java.io.UnsupportedEncodingException;

import java.security.MessageDigest;

public class Utils {
    public static String md5Java(String message){
        String digest = null;
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] hash = md.digest(message.getBytes("UTF-8"));

            //converting byte array to Hexadecimal String
            StringBuilder sb = new StringBuilder(2*hash.length);
            for(byte b : hash){
                sb.append(String.format("%02x", b&0xff));
            }

            digest = sb.toString();

        } catch (UnsupportedEncodingException ex) {
            ex.printStackTrace();
        } catch (NoSuchAlgorithmException ex) {
            ex.printStackTrace();
        }
        return digest;
    }

    public static Result getResult(String tablename, String columnFam, String columnQuant, 
            String rowkey, boolean isHashed)
    {
        try{
            Configuration conf = HBaseConfiguration.create();
            HTable table = new HTable(conf, tablename);
            String hashedKey = (isHashed)? rowkey : md5Java(rowkey);
            Get get = new Get(Bytes.toBytes(hashedKey));
            get.addColumn(Bytes.toBytes(columnFam), Bytes.toBytes(columnQuant));
            return table.get(get);
        }catch(Exception e){
            e.printStackTrace();
            return null;
        }
    }

    public static ResultScanner getResultScanner(String tablename, String columnFam, String columnQuant,
            byte[] rowkeyPrefix)
    {
        try{
            Configuration conf = HBaseConfiguration.create();
            HTable table = new HTable(conf, tablename);
            Scan scan = new Scan(rowkeyPrefix, new PrefixFilter(rowkeyPrefix));
            scan.addColumn(Bytes.toBytes(columnFam), Bytes.toBytes(columnQuant));
            return table.getScanner(scan);
        }catch(Exception e){
            e.printStackTrace();
            return null;
        }

    }

}
