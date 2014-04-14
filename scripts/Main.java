// references lab 2 work
// main java file for populating hbase table
import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.HBaseAdmin;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.util.Bytes;

import src.Utils; // see if you need this, if the hashing should happen
				  // here too even though everything is of 
				  // roughly the same length

// TODO generate makefile
class Main{
	public static void main(String[] args){
		//unpack give txt file, populate table
	}
}

	/**private static HBaseAdmin admin;

	public static void main(String[] args){
		try{
			Configuration conf = HBaseConfiguration.create();
			admin = new HBaseAdmin(conf);
		} catch (MasterNotRunningException ex){
			System.out.println("MasterNotRunningException: " + ex.getMessage());
		} catch (ZooKeeperConnectionException ex){
			System.out.println("ZooKeeperConnectionException: " + ex.getMessage());
		}
		deleteTables();
		buildTables();
        populateTables();

        // Now run the actual test code
        Queries q = new Queries();
        try{
            q.run();
        }catch(Exception e){
            e.printStackTrace();
        }
        
	}

	public static void deleteTables(){
		try{
            admin.disableTable("posts");
            admin.deleteTable("posts");

			admin.disableTable("users");
			admin.deleteTable("users");

            admin.disableTable("likes");
            admin.deleteTable("likes");

            admin.disableTable("comments");
            admin.deleteTable("comments");
		} catch(IOException ex){
			System.out.println("IOException: " + ex.getMessage());
		}
	}
	
	//remember to start hbase before you run this code
	public static void buildTables(){
		try{
            HTableDescriptor postsTableDescriptor = new HTableDescriptor("posts");
            postsTableDescriptor.addFamily(new HColumnDescriptor("info"));
            postsTableDescriptor.addFamily(new HColumnDescriptor("comment"));
            admin.createTable(postsTableDescriptor);

			HTableDescriptor usersTableDescriptor = new HTableDescriptor("users");
			usersTableDescriptor.addFamily(new HColumnDescriptor("info"));
            usersTableDescriptor.addFamily(new HColumnDescriptor("friends"));
			admin.createTable(usersTableDescriptor);

            HTableDescriptor likesTableDescriptor = new HTableDescriptor("likes");
            likesTableDescriptor.addFamily(new HColumnDescriptor("likers"));
            admin.createTable(likesTableDescriptor);

            HTableDescriptor commentsTableDescriptor = new HTableDescriptor("comments");
            commentsTableDescriptor.addFamily(new HColumnDescriptor("info"));
            admin.createTable(commentsTableDescriptor);

			//build flesh
			//HTable table = new HTable(admin.getConfiguration(),"test");
			//Put put = new Put(Bytes.toBytes("test-tacular"));
			//put.add(Bytes.toBytes("quiz"),Bytes.toBytes("quizzical"),Bytes.toBytes("end-of-the-year"));
			//table.put(put);
			//table.flushCommits();
			//table.close();

			//Get get = new Get(Bytes.toBytes("test-tacular"));
			//get.addFamily(Bytes.toBytes("quiz"));
			//get.setMaxVersions(3);
			//Result result = table.get(get);
			//System.out.println("results: " + result.toString());
		} catch(IOException ex){
			System.out.println("IOException: " + ex.getMessage());
		}
	}

    //fill tables with fake data
    public static void populateTables(){
        try{
            String md5Dean = Utils.md5Java("u1");
            String md5Sam = Utils.md5Java("u2");
            String md5Castiel = Utils.md5Java("u3");
            
            // populate users
            HTable usersTable = new HTable(admin.getConfiguration(), "users");

            Put putDean = new Put(Bytes.toBytes(md5Dean));
            populateRow(putDean,"info",  "name",    "Dean");
            populateRow(putDean,"info",  "partnerId",md5Castiel);
            populateRow(putDean,"friends",md5Sam,    "");
            populateRow(putDean,"friends",md5Castiel,"");
            usersTable.put(putDean);

            Put putSam = new Put(Bytes.toBytes(md5Sam));
            populateRow(putSam,"info",  "name",     "Sam");
            populateRow(putSam,"info",  "partnerId", "");
            populateRow(putSam,"friends",md5Dean,    "");
            populateRow(putSam,"friends",md5Castiel, "");
            usersTable.put(putSam);

            Put putCastiel = new Put(Bytes.toBytes(md5Castiel));
            populateRow(putCastiel,"info",  "name",    "Castiel");
            populateRow(putCastiel,"info",  "partnerId",md5Dean);
            populateRow(putCastiel,"friends",md5Dean,   "");
            populateRow(putCastiel,"friends",md5Sam,    "");
            usersTable.put(putCastiel);

            usersTable.flushCommits();
            usersTable.close();

            //populate posts
            HTable postsTable = new HTable(admin.getConfiguration(), "posts");
            String md5Post1 = Utils.md5Java("p1");
            Put putDeanPost = new Put(Bytes.toBytes("" + md5Dean + md5Post1));
            populateRow(putDeanPost,"info","content","Man, I look like one of the Blues Brothers.");
            populateRow(putDeanPost,"info","shareId",md5Sam);
            postsTable.put(putDeanPost);

            Put putSamPostLike = new Put(Bytes.toBytes("" + md5Dean + md5Post1 + md5Sam));
            populateRow(putSamPostLike,"info","content","");
            postsTable.put(putSamPostLike);

            postsTable.flushCommits();
            postsTable.close();

            //populate comments
            HTable commentsTable = new HTable(admin.getConfiguration(),"comments");
            Put putSamPostComment = new Put(Bytes.toBytes("" + md5Dean + md5Post1 + md5Sam));
            populateRow(putSamPostComment,"info","content","You look more like a seventh grader at his first dance.");
	    populateRow(putSamPostComment,"info", "author", "u2");
            commentsTable.put(putSamPostComment);

            commentsTable.flushCommits();
            commentsTable.close();

            //populate likes
            HTable likesTable = new HTable(admin.getConfiguration(),"likes");
            Put putSamLike = new Put(Bytes.toBytes("" + md5Dean + md5Post1 + "p"));
            populateRow(putSamLike,"likers",md5Sam,"");
            likesTable.put(putSamLike);

            Put putCasLike = new Put(Bytes.toBytes("" + md5Dean + md5Post1 + md5Sam + "c"));
            populateRow(putCasLike,"likers",md5Castiel,"");
            likesTable.put(putCasLike);

            likesTable.flushCommits();
            likesTable.close();
        }catch(IOException ex){
            System.out.println("IOException: " + ex.getMessage());
        }
    }

    public static void populateRow(Put put, String columnFamily, String columnQualifier, String value){
        put.add(Bytes.toBytes(columnFamily),Bytes.toBytes(columnQualifier),Bytes.toBytes(value));
    } **/