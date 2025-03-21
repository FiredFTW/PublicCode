import java.io.*;

public class CardInputStream extends InputStream{
    BufferedReader reader;

    public CardInputStream(InputStream input){
        reader = new BufferedReader(new InputStreamReader(input));
    } 

    public Card readCard(){
        try {
            
            //read data for single card and create an object
            if (!(reader.readLine().equals("CARD"))){
                return null;
            } 

            long id = Long.parseLong(reader.readLine());
            String name = reader.readLine();
            Rank rank = Rank.valueOf(reader.readLine());
            long price = Long.parseLong(reader.readLine());
            return new Card(id,name,rank,price);

            
        } catch (IOException e){
            System.out.println("unable to read card");
            return null;
        }


    }

    public String readResponse(){
        try {
            return reader.readLine();
        } catch (IOException e){
            System.out.println("unable to read line");
            return null;
        }
       
    }

    @Override
    public void close(){
        try {
            reader.close();
        } catch (IOException e){
            System.out.println("unable to close stream");
        }
        
    }

    @Override
    public int read(){
        return -1;
    }
}