import java.io.IOException;
import java.util.HashSet;
import java.util.Scanner;
import java.io.File;
import java.lang.String;
import java.util.ArrayList;
import java.util.List;

import com.mongodb.MongoClient;
import com.mongodb.MongoException;
import com.mongodb.WriteConcern;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;
import com.mongodb.DBCursor;
import com.mongodb.ServerAddress;
import java.util.Arrays;

class Mongo{
	public static void main(String[] args){
		try{
			// To connect to mongodb server
			MongoClient mongoClient = new MongoClient( "localhost" , 27017 );
			
			// Now connect to your databases
			DB db = mongoClient.getDB("test");
			System.out.println("Connect to database successfully");
			//boolean auth = db.authenticate(myUserName, myPassword);
			//System.out.println("Authentication: "+auth);
			DBObject options = new BasicDBObject("id", "0").
					append("trackID", "0").
					append("songID", "0").
					append("artist", "0").
					append("title", "0");
			DBCollection coll = db.getCollection("msdinfo");
			System.out.println("Collection created successfully");
			
            //open duplicates file and load into set
            Scanner in = new Scanner(new File("msd_duplicates.txt"));
            String line = "";
            String[] splitLine;
            String songtitle = "";
            HashSet<String> duplicates = new HashSet<String>();
			while (in.hasNextLine()) {
				line = in.nextLine();
				splitLine = line.split(" ");
				if (Character.isLetter(splitLine[0].charAt(0)))
					duplicates.add(splitLine[0]);
			}
			
			// populate table
			in = new Scanner(new File("data.txt")); // **change source file name
			List<DBObject> docs = new ArrayList<>();
			
			while (in.hasNextLine()) {
				line = in.nextLine();
				// format: key - trackFileName - songID - artistName - songTitle
				splitLine = line.split("\\t");
				if (!duplicates.contains(splitLine[1])) {
					if (splitLine.length == 5)
						songtitle = splitLine[4];
					else
						songtitle = "Untitled";
					DBObject doc = new BasicDBObject("id", splitLine[0]).
							append("trackID", splitLine[1]).
							append("songID", splitLine[2]).
							append("artist", splitLine[3]).
							append("title", songtitle);
					if (docs.size() < 1000)
						docs.add(doc);
					else {
						coll.insert(docs);
						docs.clear();
						docs.add(doc);
					}
				}
			}
			
		} catch(Exception e){
			System.err.println( e.getClass().getName() + ": " + e.getMessage() );
		}
	}
}

