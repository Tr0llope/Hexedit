import java.util.*;
import java.io.*;
import java.net.*;

public class CalcUI{
	boolean log_recording;
	boolean log_playing;
	public static BufferedReader ins;
	public static PrintStream outs;
	
	public CalcUI(String[] args) throws IOException{
		initStreams(args);
		mainLoop();
	}
	
	public void initStreams(String[] args) throws IOException{
		boolean local = false;
		boolean	remote = false;
		for(String s: args){
			switch(s){
				case "local":
					local = true;
					break;
				case "remote":
					remote = true;
					break;
				case "log":
					log_recording = true;
					break;
				case "replay":
					log_playing = true;
					break;
			}
		}
		if(local) initFullLocal();
		if(remote){
			initFullRemote();
		} 
		if(local && log_playing) initReplayLocal();
		if(remote && log_playing) initReplayRemote();
		
	}
	
	public void initFullLocal(){
		ins = new BufferedReader(new InputStreamReader(System.in));
		outs = System.out;
	}
	public void initFullRemote() throws IOException{
		ServerSocket serversocket = new ServerSocket(4040);
		Socket socket = serversocket.accept();
		ins = new BufferedReader(new InputStreamReader(socket.getInputStream()));
		outs = new PrintStream( socket.getOutputStream());
		/*int port = 12345;
		ServerSocket receptionniste;
		Socket socket;

		try {
			receptionniste = new ServerSocket( port );
			while( true ) {
				System.out.println( "waiting..." );
				socket = receptionniste.accept();
				System.out.println( "connexion!" );
				ServerService service = new ServerService( socket );
			}
		} catch( IOException e ) {
			System.out.println( "problème de connexion" );
		}*/
	}
	
	public void initReplayLocal(){
		try {
			ins = new BufferedReader(new FileReader("log.txt"));
		} catch (Exception e) {
			return;
		}
		outs = System.out;
	}
	public void initReplayRemote() throws IOException{
		ServerSocket serversocket = new ServerSocket(12345);
		Socket socket = serversocket.accept();
		ins = new BufferedReader(new FileReader("log.txt"));
		outs = new PrintStream(socket.getOutputStream());
	}

	public void parser(String input, PileRPL pile){
		String[] command = input.split(" ");
		for(int i = 0; i<command.length;i++){
			switch(command[i]){
				case "push":
					i+=1;
					String [] elem2D = command[i].split(",");
					if(elem2D.length == 1){
						ObjEmp o = new ObjEmp(Integer.parseInt(elem2D[0]));
						pile.push(o);
					}
					else if(elem2D.length == 2){
						ObjEmp o = new ObjEmp(Integer.parseInt(elem2D[0]), Integer.parseInt(elem2D[1]));
						pile.push(o);
					}
					else{
						ObjEmp o = new ObjEmp(Integer.parseInt(elem2D[0]), Integer.parseInt(elem2D[1]), Integer.parseInt(elem2D[2]));
						pile.push(o);
					}
					break;

				case "add":
					pile.ope("add");
					break;

				case "sub":
					pile.ope("sub");
					break;
				case "mul":
					pile.ope("mul");
					break;
				case "div":
					pile.ope("div");
					break;
			}
		}
	}

	public void mainLoop(){
		File logfile = null;
		FileWriter flog = null;
		BufferedWriter bufflog = null;
		try{
				if(log_recording){
					logfile = new File("log.txt");
					flog = new FileWriter(logfile.getAbsoluteFile());
					bufflog = new BufferedWriter(flog);
					outs.println("Logged Session !");
				}

		outs.println("Bienvenue dans la calculatrice RPL !\n" + //
				"Taille de la pile:");
		Scanner sc = new Scanner(ins);
		String input = sc.nextLine();
		int taille = Integer.parseInt(input);
		PileRPL pile = new PileRPL(taille);

		while(!input.equals("quit")){
			if(log_recording) bufflog.write(input+"\n");
			if(log_playing) outs.println(input);
			parser(input, pile);

		if(!pile.isEmpty()){
			outs.println(pile);
		}
		input = sc.nextLine();
	}
	bufflog.close();
	}catch (Exception e){return;}
}
}
